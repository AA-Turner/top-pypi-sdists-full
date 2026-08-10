use crate::{JSONTools, JsonOutput};
use serde_json::Value;

/// Helper function to extract single result from JsonOutput
#[cfg(test)]
pub fn extract_single(output: JsonOutput) -> String {
    match output {
        JsonOutput::Single(result) => result,
        JsonOutput::Multiple(_) => panic!("Expected single result but got multiple"),
    }
}

/// Helper function to extract multiple results from JsonOutput
#[cfg(test)]
pub fn extract_multiple(output: JsonOutput) -> Vec<String> {
    match output {
        JsonOutput::Single(_) => panic!("Expected multiple results but got single"),
        JsonOutput::Multiple(results) => results,
    }
}

#[cfg(test)]
mod unit_tests {
    use super::*;

    // ===== BASIC FUNCTIONALITY TESTS =====

    #[test]
    fn test_basic_flattening() {
        let json = r#"{"a": {"b": {"c": 1}}}"#;
        let result = JSONTools::new().flatten().execute(json).unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        assert_eq!(parsed["a.b.c"], 1);
    }

    #[test]
    fn test_basic_unflattening() {
        let flattened = r#"{"user.name": "John", "user.age": 30}"#;
        let result = JSONTools::new().unflatten().execute(flattened).unwrap();
        let unflattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&unflattened).unwrap();

        assert_eq!(parsed["user"]["name"], "John");
        assert_eq!(parsed["user"]["age"], 30);
    }

    #[test]
    fn test_array_flattening() {
        let json = r#"{"items": [1, 2, {"nested": "value"}]}"#;
        let result = JSONTools::new().flatten().execute(json).unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        assert_eq!(parsed["items.0"], 1);
        assert_eq!(parsed["items.1"], 2);
        assert_eq!(parsed["items.2.nested"], "value");
    }

    #[test]
    fn test_array_unflattening() {
        let flattened = r#"{"items.0": 1, "items.1": 2, "items.2.nested": "value"}"#;
        let result = JSONTools::new().unflatten().execute(flattened).unwrap();
        let unflattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&unflattened).unwrap();

        assert_eq!(parsed["items"][0], 1);
        assert_eq!(parsed["items"][1], 2);
        assert_eq!(parsed["items"][2]["nested"], "value");
    }

    // ===== CONFIGURATION TESTS =====

    #[test]
    fn test_custom_separator() {
        let json = r#"{"user": {"name": "John", "age": 30}}"#;
        let result = JSONTools::new()
            .flatten()
            .separator("::")
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        assert_eq!(parsed["user::name"], "John");
        assert_eq!(parsed["user::age"], 30);
    }

    #[test]
    fn test_default_and_explicit_dot_separator_match() {
        // Regression guard for the `separator: Cow<'static, str>` change --
        // the default separator (a `Cow::Borrowed(".")`) and an explicit
        // `.separator(".")` call (which now special-cases back to the same
        // `Cow::Borrowed(".")` in the setter) must produce byte-identical
        // output to each other and to the pre-change `String`-based
        // behavior.
        let json = r#"{"user": {"name": "John", "age": 30}}"#;

        let default_result = JSONTools::new().flatten().execute(json).unwrap();
        let explicit_dot_result = JSONTools::new()
            .flatten()
            .separator(".")
            .execute(json)
            .unwrap();

        assert_eq!(
            extract_single(default_result),
            extract_single(explicit_dot_result)
        );

        let flattened = extract_single(JSONTools::new().flatten().execute(json).unwrap());
        let parsed: Value = serde_json::from_str(&flattened).unwrap();
        assert_eq!(parsed["user.name"], "John");
        assert_eq!(parsed["user.age"], 30);
    }

    #[test]
    fn test_lowercase_keys() {
        let json = r#"{"User": {"Name": "John", "Email": "john@example.com"}}"#;
        let result = JSONTools::new()
            .flatten()
            .lowercase_keys(true)
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        assert_eq!(parsed["user.name"], "John");
        assert_eq!(parsed["user.email"], "john@example.com");
    }

    #[test]
    fn test_key_replacement() {
        let json = r#"{"user_name": "John", "admin_role": "super"}"#;
        let result = JSONTools::new()
            .flatten()
            .key_replacement("user_", "")
            .key_replacement("admin_", "")
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        assert_eq!(parsed["name"], "John");
        assert_eq!(parsed["role"], "super");
    }

    #[test]
    fn test_exclude_key_drops_container_subtree_flatten() {
        // Matching a container key ("crypto_wallet") must drop its entire subtree
        // without the leaf keys ("coin", "balance") ever needing to individually match.
        let json =
            r#"{"user": {"name": "John", "crypto_wallet": {"coin": "BTC", "balance": 100}}}"#;
        let result = JSONTools::new()
            .flatten()
            .exclude_key("crypto")
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert_eq!(parsed["user.name"], "John");
        let keys: Vec<&str> = parsed
            .as_object()
            .unwrap()
            .keys()
            .map(|s| s.as_str())
            .collect();
        assert!(!keys.iter().any(|k| k.contains("crypto")));
        assert_eq!(keys.len(), 1);
    }

    #[test]
    fn test_exclude_key_drops_leaf_flatten() {
        let json = r#"{"user": {"name": "John", "crypto_balance": 100, "city": "NYC"}}"#;
        let result = JSONTools::new()
            .flatten()
            .exclude_key("crypto")
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert_eq!(parsed["user.name"], "John");
        assert_eq!(parsed["user.city"], "NYC");
        assert!(!parsed
            .as_object()
            .unwrap()
            .contains_key("user.crypto_balance"));
    }

    #[test]
    fn test_exclude_key_drops_container_subtree_unflatten() {
        let flat_json = r#"{"user.name": "John", "user.crypto_wallet.coin": "BTC", "user.crypto_wallet.balance": 100}"#;
        let result = JSONTools::new()
            .unflatten()
            .exclude_key("crypto")
            .execute(flat_json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert_eq!(parsed["user"]["name"], "John");
        assert!(!parsed["user"]
            .as_object()
            .unwrap()
            .contains_key("crypto_wallet"));
    }

    #[test]
    fn test_exclude_key_drops_container_subtree_normal() {
        let json =
            r#"{"user": {"name": "John", "crypto_wallet": {"coin": "BTC", "balance": 100}}}"#;
        let result = JSONTools::new()
            .normal()
            .exclude_key("crypto")
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert_eq!(parsed["user"]["name"], "John");
        assert!(!parsed["user"]
            .as_object()
            .unwrap()
            .contains_key("crypto_wallet"));
    }

    #[test]
    fn test_exclude_key_drops_leaf_normal() {
        let json = r#"{"user": {"name": "John", "crypto_balance": 100, "city": "NYC"}}"#;
        let result = JSONTools::new()
            .normal()
            .exclude_key("crypto")
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert_eq!(parsed["user"]["name"], "John");
        assert_eq!(parsed["user"]["city"], "NYC");
        assert!(!parsed["user"]
            .as_object()
            .unwrap()
            .contains_key("crypto_balance"));
    }

    #[test]
    fn test_exclude_key_regex_pattern() {
        let json = r#"{"cryptoBalance": 100, "cryptoWallet": "abc", "name": "John"}"#;
        let result = JSONTools::new()
            .flatten()
            .exclude_key("r'^crypto'")
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert_eq!(parsed["name"], "John");
        assert!(!parsed.as_object().unwrap().contains_key("cryptoBalance"));
        assert!(!parsed.as_object().unwrap().contains_key("cryptoWallet"));
    }

    #[test]
    fn test_exclude_key_multiple_additive() {
        let json = r#"{"crypto_balance": 100, "secret_token": "x", "name": "John"}"#;
        let result = JSONTools::new()
            .flatten()
            .exclude_key("crypto")
            .exclude_key("secret")
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert_eq!(parsed["name"], "John");
        assert_eq!(parsed.as_object().unwrap().len(), 1);
    }

    #[test]
    fn test_exclude_key_combined_with_other_filters() {
        let json =
            r#"{"crypto_balance": 100, "status": "N/A", "verified": "true", "name": "John"}"#;
        let result = JSONTools::new()
            .flatten()
            .exclude_key("crypto")
            .auto_convert_types(true)
            .remove_nulls(true)
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert_eq!(parsed["name"], "John");
        assert_eq!(parsed["verified"], true);
        assert!(!parsed.as_object().unwrap().contains_key("crypto_balance"));
        assert!(!parsed.as_object().unwrap().contains_key("status")); // "N/A" -> null -> removed
    }

    #[test]
    fn test_exclude_key_never_matches_array_elements() {
        // A pattern matching a sibling object key must not affect array elements,
        // which have no key name to check against.
        let json = r#"{"crypto_tags": ["a", "b"], "items": [1, 2, 3]}"#;
        let result = JSONTools::new()
            .flatten()
            .exclude_key("crypto")
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert!(!parsed
            .as_object()
            .unwrap()
            .keys()
            .any(|k| k.contains("crypto")));
        assert_eq!(parsed["items.0"], 1);
        assert_eq!(parsed["items.1"], 2);
        assert_eq!(parsed["items.2"], 3);
    }

    #[test]
    fn test_exclude_value_string_leaf_flatten() {
        let json = r#"{"user": {"name": "John", "status": "banned"}}"#;
        let result = JSONTools::new()
            .flatten()
            .exclude_value("banned")
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert_eq!(parsed["user.name"], "John");
        assert!(!parsed.as_object().unwrap().contains_key("user.status"));
    }

    #[test]
    fn test_exclude_value_non_string_scalar() {
        // Matches against the textual form of a raw (non-string) JSON scalar.
        let json = r#"{"a": 42, "b": true, "c": "keep"}"#;
        let result = JSONTools::new()
            .flatten()
            .exclude_value("42")
            .exclude_value("true")
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert_eq!(parsed["c"], "keep");
        assert!(!parsed.as_object().unwrap().contains_key("a"));
        assert!(!parsed.as_object().unwrap().contains_key("b"));
    }

    #[test]
    fn test_exclude_value_string_leaf_unflatten() {
        let flat_json = r#"{"user.name": "John", "user.status": "banned"}"#;
        let result = JSONTools::new()
            .unflatten()
            .exclude_value("banned")
            .execute(flat_json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert_eq!(parsed["user"]["name"], "John");
        assert!(!parsed["user"].as_object().unwrap().contains_key("status"));
    }

    #[test]
    fn test_exclude_value_string_leaf_normal() {
        let json = r#"{"user": {"name": "John", "status": "banned"}}"#;
        let result = JSONTools::new()
            .normal()
            .exclude_value("banned")
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert_eq!(parsed["user"]["name"], "John");
        assert!(!parsed["user"].as_object().unwrap().contains_key("status"));
    }

    #[test]
    fn test_exclude_value_regex_and_multiple() {
        let json = r#"{"a": "foo-bar", "b": "secret-x", "c": "keep"}"#;
        let result = JSONTools::new()
            .flatten()
            .exclude_value("r'^foo-'")
            .exclude_value("secret")
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert_eq!(parsed, serde_json::json!({"c": "keep"}));
    }

    #[test]
    fn test_exclude_value_only_matches_after_replacement() {
        // Direct analog of the remove_nulls ordering regression test: exclude_value
        // must see the *replaced* value, not the pre-replacement original text. "a"'s
        // original text ("temp_flag") doesn't contain "banned" at all -- only the
        // replacement's output does.
        let json = r#"{"a": "temp_flag", "b": "keep"}"#;
        let result = JSONTools::new()
            .flatten()
            .value_replacement("temp_flag", "banned_user")
            .exclude_value("banned")
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert_eq!(parsed["b"], "keep");
        assert!(!parsed.as_object().unwrap().contains_key("a"));
    }

    #[test]
    fn test_exclude_value_matches_after_replacement_and_conversion() {
        // Full chain: replacement produces "999" (a string), auto_convert_types
        // converts it to the number 999, and exclude_value checks that *converted*
        // value's textual form.
        let json = r#"{"a": "old_price", "b": "keep"}"#;
        let result = JSONTools::new()
            .flatten()
            .value_replacement("old_price", "999")
            .auto_convert_types(true)
            .exclude_value("999")
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert_eq!(parsed["b"], "keep");
        assert!(!parsed.as_object().unwrap().contains_key("a"));
    }

    #[test]
    fn test_exclude_value_combined_with_remove_nulls_and_exclude_key() {
        let json = r#"{"crypto_wallet": {"coin": "BTC"}, "status": null, "flagged": "yes", "name": "John"}"#;
        let result = JSONTools::new()
            .flatten()
            .exclude_key("crypto")
            .exclude_value("yes")
            .remove_nulls(true)
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert_eq!(parsed, serde_json::json!({"name": "John"}));
    }

    #[test]
    fn test_exclude_value_never_checks_container_values() {
        // A pattern that would match a nested leaf's serialized form must not cause
        // the parent container itself to be dropped wholesale -- only the specific
        // scalar leaf matching is removed.
        let json = r#"{"wallet": {"coin": "flagged", "amount": 5}}"#;
        let result = JSONTools::new()
            .flatten()
            .exclude_value("flagged")
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert_eq!(parsed["wallet.amount"], 5);
        assert!(!parsed.as_object().unwrap().contains_key("wallet.coin"));
    }

    #[test]
    fn test_exclude_value_noop_at_document_root() {
        let result = JSONTools::new()
            .flatten()
            .exclude_value("banned")
            .execute(r#""banned""#)
            .unwrap();
        assert_eq!(extract_single(result), "\"banned\"");
    }

    #[test]
    fn test_exclude_value_unflatten_matches_serialized_quoted_form() {
        // Documents the unflatten-specific caveat: string values are matched against
        // their JSON-serialized (quoted) form, not the unescaped logical text. A
        // literal pattern is unaffected; a regex needs to account for the quotes.
        let flat_json = r#"{"a": "admin", "b": "keep"}"#;

        let literal_result = JSONTools::new()
            .unflatten()
            .exclude_value("admin")
            .execute(flat_json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(literal_result)).unwrap();
        assert_eq!(parsed, serde_json::json!({"b": "keep"}));

        // Bare-anchored regex does NOT match, because the compared text includes
        // the surrounding quotes: `"admin"`, not `admin`.
        let bare_anchor_result = JSONTools::new()
            .unflatten()
            .exclude_value("r'^admin$'")
            .execute(flat_json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(bare_anchor_result)).unwrap();
        assert_eq!(parsed, serde_json::json!({"a": "admin", "b": "keep"}));

        // Quote-aware anchored regex DOES match.
        let quoted_anchor_result = JSONTools::new()
            .unflatten()
            .exclude_value(r#"r'^"admin"$'"#)
            .execute(flat_json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(quoted_anchor_result)).unwrap();
        assert_eq!(parsed, serde_json::json!({"b": "keep"}));
    }

    /// Regression test for `memmem_replace_all` in transform.rs: multiple
    /// non-overlapping occurrences of the same literal pattern in one key, and a
    /// replacement string that itself contains the search pattern (must not
    /// re-match the just-inserted text, matching `str::replace`'s semantics of
    /// scanning the original string, not the growing output).
    #[test]
    fn test_literal_replacement_multiple_and_self_referential() {
        let json = r#"{"admin_admin_admin": 1, "xx": 2}"#;
        let result = JSONTools::new()
            .flatten()
            .key_replacement("admin", "root")
            .key_replacement("x", "xx")
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        assert_eq!(parsed["root_root_root"], 1);
        // "xx" -> each 'x' replaced with "xx" against the *original* string,
        // not re-matched against inserted output: "xx" -> "xxxx", not infinite.
        assert_eq!(parsed["xxxx"], 2);
    }

    /// An empty literal pattern is legal but degenerate input (no config-time
    /// validation rejects it); must not hang or panic, and should match
    /// `str::replace("", ..)`'s defined (if unusual) zero-width-everywhere behavior.
    #[test]
    fn test_literal_replacement_empty_pattern_does_not_hang() {
        let json = r#"{"ab": 1}"#;
        let result = JSONTools::new()
            .flatten()
            .key_replacement("", "-")
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        assert_eq!(parsed["-a-b-"], 1);
    }

    #[test]
    fn test_value_replacement() {
        let json = r#"{"email": "john@example.com", "role": "super"}"#;
        let result = JSONTools::new()
            .flatten()
            .value_replacement("@example.com", "@company.org")
            .value_replacement("super", "administrator")
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        assert_eq!(parsed["email"], "john@company.org");
        assert_eq!(parsed["role"], "administrator");
    }

    #[test]
    fn test_regex_replacements() {
        let json = r#"{"user_name": "John", "admin_role": "super", "temp_data": "test"}"#;
        let result = JSONTools::new()
            .flatten()
            .key_replacement("r'^(user|admin)_'", "")
            .value_replacement("r'^super$'", "administrator")
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        assert_eq!(parsed["name"], "John");
        assert_eq!(parsed["role"], "administrator");
        assert_eq!(parsed["temp_data"], "test");
    }

    #[test]
    fn test_bare_pattern_with_regex_metacharacters_is_literal() {
        // Regression test: patterns are only regex when explicitly wrapped in r'...'.
        // A bare pattern containing regex metacharacters (. $ ( ) etc.) must match those
        // characters literally, not as regex syntax -- e.g. "." must not match "any char".
        let json = r#"{"price": "$100", "note": "a.b.c", "status": "end$"}"#;
        let result = JSONTools::new()
            .flatten()
            // "$" is a regex end-anchor if compiled as regex; as a literal it must match
            // the literal dollar sign in "$100" and nowhere else.
            .value_replacement("$100", "USD 100")
            // "." is "any character" as regex; as a literal it must only match a real dot.
            .key_replacement("note", "dotted")
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();

        assert_eq!(parsed["price"], "USD 100");
        assert_eq!(parsed["dotted"], "a.b.c");
        // "end$" is untouched: the literal pattern "$100" doesn't appear in it.
        assert_eq!(parsed["status"], "end$");
    }

    #[test]
    fn test_r_quote_wrapped_pattern_is_regex() {
        let json = r#"{"a.b.c": "x"}"#;
        // "." unwrapped would only match a literal dot; r'.' means "any character".
        let result = JSONTools::new()
            .unflatten()
            .value_replacement("r'.'", "Y")
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        // Every character of "x" (just one char) gets replaced -- confirms regex semantics.
        assert_eq!(parsed["a"]["b"]["c"], "Y");
    }

    #[test]
    fn test_malformed_r_quote_regex_is_silently_ignored() {
        // An r'...'-wrapped pattern that fails to compile as regex is treated as "no
        // match" for that pattern rather than erroring -- there's no config-time
        // validation point for replacement patterns.
        let json = r#"{"key": "value"}"#;
        let result = JSONTools::new()
            .flatten()
            .key_replacement("r'[invalid'", "replacement")
            .value_replacement("r'*invalid'", "replacement")
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert_eq!(parsed["key"], "value");
    }

    #[test]
    fn test_r_quote_pattern_edge_cases() {
        // Too short to be a valid r'...' wrapper (would panic on naive slicing if the
        // length guard were missing) -- both fall back to being literal 2-character text.
        let json = r#"{"a": "r'", "b": "not it"}"#;
        let result = JSONTools::new()
            .flatten()
            .value_replacement("r'", "X")
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert_eq!(parsed["a"], "X"); // literal "r'" matched and replaced
        assert_eq!(parsed["b"], "not it");

        // r''  (empty regex) is a valid, if unusual, wrapped pattern -- matches everywhere,
        // inserting the replacement before every character (and at the end).
        let json2 = r#"{"a": "hi"}"#;
        let result2 = JSONTools::new()
            .flatten()
            .value_replacement("r''", "-")
            .execute(json2)
            .unwrap();
        let parsed2: Value = serde_json::from_str(&extract_single(result2)).unwrap();
        assert_eq!(parsed2["a"], "-h-i-");
    }

    // ===== FILTERING TESTS =====

    #[test]
    fn test_remove_empty_strings() {
        let json = r#"{"user": {"name": "John", "bio": "", "age": 30}}"#;
        let result = JSONTools::new()
            .flatten()
            .remove_empty_strings(true)
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        assert_eq!(parsed["user.name"], "John");
        assert_eq!(parsed["user.age"], 30);
        assert!(!parsed.as_object().unwrap().contains_key("user.bio"));
    }

    #[test]
    fn test_remove_nulls() {
        let json = r#"{"user": {"name": "John", "age": null, "city": "NYC"}}"#;
        let result = JSONTools::new()
            .flatten()
            .remove_nulls(true)
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        assert_eq!(parsed["user.name"], "John");
        assert_eq!(parsed["user.city"], "NYC");
        assert!(!parsed.as_object().unwrap().contains_key("user.age"));
    }

    #[test]
    fn test_remove_empty_objects() {
        let json = r#"{"user": {"name": "John", "profile": {}, "settings": {"theme": "dark"}}}"#;
        let result = JSONTools::new()
            .flatten()
            .remove_empty_objects(true)
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        assert_eq!(parsed["user.name"], "John");
        assert_eq!(parsed["user.settings.theme"], "dark");
        // Empty objects should be removed, so no user.profile keys should exist
        let keys: Vec<&str> = parsed
            .as_object()
            .unwrap()
            .keys()
            .map(|s| s.as_str())
            .collect();
        assert!(!keys.iter().any(|k| k.starts_with("user.profile")));
    }

    #[test]
    fn test_remove_empty_arrays() {
        let json = r#"{"user": {"name": "John", "tags": [], "items": [1, 2]}}"#;
        let result = JSONTools::new()
            .flatten()
            .remove_empty_arrays(true)
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        assert_eq!(parsed["user.name"], "John");
        assert_eq!(parsed["user.items.0"], 1);
        assert_eq!(parsed["user.items.1"], 2);
        // Empty arrays should be removed
        let keys: Vec<&str> = parsed
            .as_object()
            .unwrap()
            .keys()
            .map(|s| s.as_str())
            .collect();
        assert!(!keys.iter().any(|k| k.starts_with("user.tags")));
    }

    // ===== ADVANCED TESTS =====

    #[test]
    fn test_all_features_combined() {
        let json = r#"{"user_profile": {"user_name": "John", "user_email": "john@example.com", "user_age": null, "user_bio": "", "user_tags": []}}"#;
        let result = JSONTools::new()
            .flatten()
            .separator("::")
            .lowercase_keys(true)
            .key_replacement("user_", "")
            .value_replacement("@example.com", "@company.org")
            .remove_empty_strings(true)
            .remove_nulls(true)
            .remove_empty_objects(true)
            .remove_empty_arrays(true)
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        assert_eq!(parsed["profile::name"], "John");
        assert_eq!(parsed["profile::email"], "john@company.org");
        // Empty values should be removed
        assert!(!parsed.as_object().unwrap().contains_key("profile::age"));
        assert!(!parsed.as_object().unwrap().contains_key("profile::bio"));
        assert!(!parsed.as_object().unwrap().contains_key("profile::tags"));
    }

    #[test]
    fn test_roundtrip_compatibility() {
        let original =
            r#"{"user": {"name": "John", "age": 30}, "items": [1, 2, {"nested": "value"}]}"#;

        // Flatten
        let flattened_result = JSONTools::new().flatten().execute(original).unwrap();
        let flattened = extract_single(flattened_result);

        // Unflatten
        let unflattened_result = JSONTools::new().unflatten().execute(&flattened).unwrap();
        let unflattened = extract_single(unflattened_result);

        // Parse both original and result
        let original_parsed: Value = serde_json::from_str(original).unwrap();
        let result_parsed: Value = serde_json::from_str(&unflattened).unwrap();

        assert_eq!(original_parsed, result_parsed);
    }

    // ===== BATCH PROCESSING TESTS =====

    #[test]
    fn test_multiple_input_flatten() {
        let json_list = vec![
            r#"{"user": {"name": "John"}}"#,
            r#"{"user": {"name": "Jane"}}"#,
        ];

        let result = JSONTools::new()
            .flatten()
            .execute(json_list.as_slice())
            .unwrap();

        let results = extract_multiple(result);
        assert_eq!(results.len(), 2);

        let parsed1: Value = serde_json::from_str(&results[0]).unwrap();
        let parsed2: Value = serde_json::from_str(&results[1]).unwrap();

        assert_eq!(parsed1["user.name"], "John");
        assert_eq!(parsed2["user.name"], "Jane");
    }

    #[test]
    fn test_multiple_input_unflatten() {
        let flattened_list = vec![r#"{"user.name": "John"}"#, r#"{"user.name": "Jane"}"#];

        let result = JSONTools::new()
            .unflatten()
            .execute(flattened_list.as_slice())
            .unwrap();

        let results = extract_multiple(result);
        assert_eq!(results.len(), 2);

        let parsed1: Value = serde_json::from_str(&results[0]).unwrap();
        let parsed2: Value = serde_json::from_str(&results[1]).unwrap();

        assert_eq!(parsed1["user"]["name"], "John");
        assert_eq!(parsed2["user"]["name"], "Jane");
    }

    // ===== ERROR HANDLING TESTS =====

    #[test]
    fn test_error_no_mode_set() {
        let json = r#"{"user": {"name": "John"}}"#;
        let result = JSONTools::new().execute(json);

        assert!(result.is_err());
        let error_msg = result.unwrap_err().to_string();
        assert!(error_msg.contains("Operation mode not set"));
    }

    #[test]
    fn test_invalid_json() {
        let invalid_json = r#"{"user": {"name": "John"}"#; // Missing closing brace
        let result = JSONTools::new().flatten().execute(invalid_json);

        assert!(result.is_err());
    }

    // ===== UNFLATTEN FILTERING TESTS =====

    #[test]
    fn test_unflatten_remove_empty_strings() {
        let flattened = r#"{"user.name": "John", "user.bio": "", "user.age": 30}"#;
        let result = JSONTools::new()
            .unflatten()
            .remove_empty_strings(true)
            .execute(flattened)
            .unwrap();
        let unflattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&unflattened).unwrap();

        assert_eq!(parsed["user"]["name"], "John");
        assert_eq!(parsed["user"]["age"], 30);
        assert!(!parsed["user"].as_object().unwrap().contains_key("bio"));
    }

    #[test]
    fn test_unflatten_remove_nulls() {
        let flattened = r#"{"user.name": "John", "user.age": null, "user.city": "NYC"}"#;
        let result = JSONTools::new()
            .unflatten()
            .remove_nulls(true)
            .execute(flattened)
            .unwrap();
        let unflattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&unflattened).unwrap();

        assert_eq!(parsed["user"]["name"], "John");
        assert_eq!(parsed["user"]["city"], "NYC");
        assert!(!parsed["user"].as_object().unwrap().contains_key("age"));
    }

    #[test]
    fn test_unflatten_remove_empty_objects() {
        let flattened =
            r#"{"user.name": "John", "user.profile": {}, "user.settings.theme": "dark"}"#;
        let result = JSONTools::new()
            .unflatten()
            .remove_empty_objects(true)
            .execute(flattened)
            .unwrap();
        let unflattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&unflattened).unwrap();

        assert_eq!(parsed["user"]["name"], "John");
        assert_eq!(parsed["user"]["settings"]["theme"], "dark");
        assert!(!parsed["user"].as_object().unwrap().contains_key("profile"));
    }

    #[test]
    fn test_unflatten_remove_empty_arrays() {
        let flattened = r#"{"user.name": "John", "user.tags": [], "user.items.0": "first"}"#;
        let result = JSONTools::new()
            .unflatten()
            .remove_empty_arrays(true)
            .execute(flattened)
            .unwrap();
        let unflattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&unflattened).unwrap();

        assert_eq!(parsed["user"]["name"], "John");
        assert_eq!(parsed["user"]["items"][0], "first");
        assert!(!parsed["user"].as_object().unwrap().contains_key("tags"));
    }

    #[test]
    fn test_unflatten_all_filters_combined() {
        let flattened = r#"{"user.name": "John", "user.bio": "", "user.age": null, "user.profile": {}, "user.tags": [], "user.settings.theme": "dark"}"#;
        let result = JSONTools::new()
            .unflatten()
            .remove_empty_strings(true)
            .remove_nulls(true)
            .remove_empty_objects(true)
            .remove_empty_arrays(true)
            .execute(flattened)
            .unwrap();
        let unflattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&unflattened).unwrap();

        assert_eq!(parsed["user"]["name"], "John");
        assert_eq!(parsed["user"]["settings"]["theme"], "dark");
        // All empty values should be removed
        let user_obj = parsed["user"].as_object().unwrap();
        assert!(!user_obj.contains_key("bio"));
        assert!(!user_obj.contains_key("age"));
        assert!(!user_obj.contains_key("profile"));
        assert!(!user_obj.contains_key("tags"));
    }

    #[test]
    fn test_unflatten_nested_filtering() {
        let flattened = r#"{"users.0.name": "John", "users.0.bio": "", "users.1.name": "Jane", "users.1.age": null, "users.2.profile": {}}"#;
        let result = JSONTools::new()
            .unflatten()
            .remove_empty_strings(true)
            .remove_nulls(true)
            .remove_empty_objects(true)
            .execute(flattened)
            .unwrap();
        let unflattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&unflattened).unwrap();

        // Check that the structure is correct
        assert_eq!(parsed["users"][0]["name"], "John");
        assert_eq!(parsed["users"][1]["name"], "Jane");

        // Check that empty values were filtered out
        assert!(!parsed["users"][0].as_object().unwrap().contains_key("bio"));
        assert!(!parsed["users"][1].as_object().unwrap().contains_key("age"));

        // Since the empty profile object was removed, users[2] should either not exist or be empty
        // Let's check if users[2] exists and if it does, it should not have a profile key
        if let Some(user2) = parsed["users"].get(2) {
            if let Some(user2_obj) = user2.as_object() {
                assert!(!user2_obj.contains_key("profile"));
            }
        }
    }

    #[test]
    fn test_unflatten_with_replacements_and_filtering() {
        let flattened = r#"{"user_name": "John", "user_bio": "", "user_email": "john@example.com", "user_age": null}"#;
        let result = JSONTools::new()
            .unflatten()
            .key_replacement("user_", "profile.")
            .value_replacement("@example.com", "@company.org")
            .remove_empty_strings(true)
            .remove_nulls(true)
            .execute(flattened)
            .unwrap();
        let unflattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&unflattened).unwrap();

        assert_eq!(parsed["profile"]["name"], "John");
        assert_eq!(parsed["profile"]["email"], "john@company.org");
        // Empty and null values should be filtered out
        let profile_obj = parsed["profile"].as_object().unwrap();
        assert!(!profile_obj.contains_key("bio"));
        assert!(!profile_obj.contains_key("age"));
    }

    #[test]
    fn test_feature_parity_flatten_vs_unflatten() {
        // This test demonstrates that both flatten and unflatten support the same configuration methods
        let original = r#"{"user_profile": {"user_name": "John", "user_email": "john@example.com", "user_age": null, "user_bio": "", "user_tags": []}}"#;

        // Test that both operations support all the same methods
        let flatten_result = JSONTools::new()
            .flatten()
            .separator("::")
            .lowercase_keys(true)
            .key_replacement("user_", "")
            .value_replacement("@example.com", "@company.org")
            .remove_empty_strings(true)
            .remove_nulls(true)
            .remove_empty_objects(true)
            .remove_empty_arrays(true)
            .execute(original)
            .unwrap();

        let unflatten_result = JSONTools::new()
            .unflatten()
            .separator("::")
            .lowercase_keys(true)
            .key_replacement("user_", "")
            .value_replacement("@company.org", "@example.com")
            .remove_empty_strings(true)
            .remove_nulls(true)
            .remove_empty_objects(true)
            .remove_empty_arrays(true)
            .execute(r#"{"profile::name": "John", "profile::email": "john@company.org", "profile::bio": "", "profile::age": null, "profile::tags": []}"#)
            .unwrap();

        // Both operations should succeed and produce valid JSON
        let flattened = extract_single(flatten_result);
        let unflattened = extract_single(unflatten_result);

        let flattened_parsed: Value = serde_json::from_str(&flattened).unwrap();
        let unflattened_parsed: Value = serde_json::from_str(&unflattened).unwrap();

        // Verify that both operations applied filtering correctly
        assert_eq!(flattened_parsed["profile::name"], "John");
        assert_eq!(flattened_parsed["profile::email"], "john@company.org");
        assert!(!flattened_parsed
            .as_object()
            .unwrap()
            .contains_key("profile::bio"));
        assert!(!flattened_parsed
            .as_object()
            .unwrap()
            .contains_key("profile::age"));
        assert!(!flattened_parsed
            .as_object()
            .unwrap()
            .contains_key("profile::tags"));

        assert_eq!(unflattened_parsed["profile"]["name"], "John");
        assert_eq!(unflattened_parsed["profile"]["email"], "john@example.com");
        let profile_obj = unflattened_parsed["profile"].as_object().unwrap();
        assert!(!profile_obj.contains_key("bio"));
        assert!(!profile_obj.contains_key("age"));
        assert!(!profile_obj.contains_key("tags"));
    }

    // ===== KEY COLLISION TESTS =====

    #[test]
    fn test_handle_key_collision_flatten_arrays() {
        let json = r#"{"User_name": "John", "Admin_name": "Jane", "Guest_name": "Bob"}"#;
        let result = JSONTools::new()
            .flatten()
            .separator("::")
            .key_replacement("r'(User|Admin|Guest)_'", "")
            .handle_key_collision(true)
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        // Should have a single key mapping to an array of values
        let obj = parsed.as_object().unwrap();
        assert_eq!(obj.len(), 1);
        assert!(obj.contains_key("name"));
        let arr = obj.get("name").unwrap().as_array().unwrap();
        assert_eq!(arr.len(), 3);
    }

    #[test]
    fn test_handle_key_collision_flatten() {
        let json = r#"{"User_name": "John", "Admin_name": "Jane", "Guest_name": "Bob"}"#;
        let result = JSONTools::new()
            .flatten()
            .key_replacement("r'(User|Admin|Guest)_'", "")
            .handle_key_collision(true)
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        // Should collect all values into an array (order may vary due to HashMap)
        if let Some(array) = parsed["name"].as_array() {
            assert_eq!(array.len(), 3);
            let values: Vec<&str> = array.iter().map(|v| v.as_str().unwrap()).collect();
            assert!(values.contains(&"John"));
            assert!(values.contains(&"Jane"));
            assert!(values.contains(&"Bob"));
        } else {
            panic!("Expected array for 'name' key");
        }
    }

    #[test]
    fn test_handle_key_collision_unflatten() {
        let flattened = r#"{"name::0": "John", "name::1": "Jane", "name::2": "Bob"}"#;
        let result = JSONTools::new()
            .unflatten()
            .separator("::")
            .key_replacement("r'name::\\d+'", "user_name")
            .handle_key_collision(true)
            .execute(flattened)
            .unwrap();
        let unflattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&unflattened).unwrap();

        // Should collect all values into an array (order may vary)
        if let Some(array) = parsed["user_name"].as_array() {
            assert_eq!(array.len(), 3);
            let values: Vec<&str> = array.iter().map(|v| v.as_str().unwrap()).collect();
            assert!(values.contains(&"John"));
            assert!(values.contains(&"Jane"));
            assert!(values.contains(&"Bob"));
        } else {
            panic!("Expected array for 'user_name' key");
        }
    }

    #[test]
    fn test_collision_precedence_collect_only() {
        // With only handle_key_collision supported, ensure colliding keys collect into arrays
        let json = r#"{"User_name": "John", "Admin_name": "Jane"}"#;
        let result = JSONTools::new()
            .flatten()
            .key_replacement("r'(User|Admin)_'", "")
            .handle_key_collision(true)
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        // Should use collect strategy (arrays)
        let obj = parsed.as_object().unwrap();
        assert_eq!(obj.len(), 1);
        assert!(obj.contains_key("name"));
        assert!(parsed["name"].is_array());

        // Check array contents
        let arr = parsed["name"].as_array().unwrap();
        assert_eq!(arr.len(), 2);
        let mut values: Vec<&str> = arr.iter().map(|v| v.as_str().unwrap()).collect();
        values.sort();
        assert_eq!(values, vec!["Jane", "John"]);
    }

    #[test]
    fn test_no_collision_no_change() {
        // When there are no collisions, and handle_key_collision is enabled, no arrays should be created
        let json = r#"{"User_name": "John", "Admin_email": "jane@example.com"}"#;
        let result = JSONTools::new()
            .flatten()
            .key_replacement("r'(User|Admin)_'", "")
            .handle_key_collision(true)
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        // No collisions, so keys should remain as-is
        assert_eq!(parsed["name"], "John");
        assert_eq!(parsed["email"], "jane@example.com");
    }

    // ===== ALWAYS-ARRAY-KEYS TESTS =====

    #[test]
    fn test_always_array_keys_wraps_single_value() {
        // No collision in this document at all, but "name" is declared
        // always-array -- it must still come out as a one-element array,
        // not a bare scalar (the whole point: consistent shape across
        // documents regardless of whether a given one happens to collide).
        let json = r#"{"User_name": "John"}"#;
        let result = JSONTools::new()
            .flatten()
            .key_replacement("r'(User|Admin)_'", "")
            .always_array_keys(["name"])
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();
        let arr = parsed["name"].as_array().unwrap();
        assert_eq!(arr, &[Value::String("John".to_string())]);
    }

    #[test]
    fn test_always_array_keys_still_collects_real_collisions() {
        let json = r#"{"User_name": "John", "Admin_name": "Jane"}"#;
        let result = JSONTools::new()
            .flatten()
            .key_replacement("r'(User|Admin)_'", "")
            .always_array_keys(["name"])
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();
        let mut values: Vec<&str> = parsed["name"]
            .as_array()
            .unwrap()
            .iter()
            .map(|v| v.as_str().unwrap())
            .collect();
        values.sort();
        assert_eq!(values, vec!["Jane", "John"]);
    }

    #[test]
    fn test_always_array_keys_works_without_handle_key_collision() {
        // always_array_keys must force full array-collection for its own
        // named key even when handle_key_collision is off (default) -- a
        // key NOT named here still falls back to last-wins in that case.
        let json = r#"{"User_name": "John", "Admin_name": "Jane", "User_age": 1, "Admin_age": 2}"#;
        let result = JSONTools::new()
            .flatten()
            .key_replacement("r'(User|Admin)_'", "")
            .always_array_keys(["name"])
            .handle_key_collision(false)
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        let mut values: Vec<&str> = parsed["name"]
            .as_array()
            .unwrap()
            .iter()
            .map(|v| v.as_str().unwrap())
            .collect();
        values.sort();
        assert_eq!(values, vec!["Jane", "John"]);
        // "age" was not declared always-array, so it keeps the ordinary
        // no-collision-handling last-wins behavior.
        assert_eq!(parsed["age"], 2);
    }

    #[test]
    fn test_always_array_keys_absent_key_stays_absent() {
        // A document that never has the always-array key at all must not
        // have it injected -- shape consistency only applies to keys that
        // are actually present.
        let json = r#"{"other": 1}"#;
        let result = JSONTools::new()
            .flatten()
            .always_array_keys(["name"])
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();
        let obj = parsed.as_object().unwrap();
        assert!(!obj.contains_key("name"));
        assert_eq!(parsed["other"], 1);
    }

    #[test]
    fn test_always_array_keys_unrelated_keys_unaffected() {
        // A key not in always_array_keys, with no collision at all, stays
        // a plain scalar -- confirms this is a per-key opt-in, not a global
        // behavior change.
        let json = r#"{"id": 42}"#;
        let result = JSONTools::new()
            .flatten()
            .always_array_keys(["name"])
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();
        assert_eq!(parsed["id"], 42);
        assert!(!parsed["id"].is_array());
    }

    #[test]
    fn test_collision_with_custom_separator() {
        let json = r#"{"User_name": "John", "Admin_name": "Jane"}"#;
        let result = JSONTools::new()
            .flatten()
            .separator("__")
            .key_replacement("r'(User|Admin)_'", "")
            .handle_key_collision(true)
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        // With custom separator in keys, but only collection strategy, we still produce arrays under a single key
        let obj = parsed.as_object().unwrap();
        assert_eq!(obj.len(), 1);
        assert!(obj.contains_key("name"));

        // Check array contents
        let arr = parsed["name"].as_array().unwrap();
        assert_eq!(arr.len(), 2);
        let mut values: Vec<&str> = arr.iter().map(|v| v.as_str().unwrap()).collect();
        values.sort();
        assert_eq!(values, vec!["Jane", "John"]);
    }

    #[test]
    fn test_collision_with_mixed_value_types() {
        let json = r#"{"User_name": "John", "Admin_name": 42, "Guest_name": true}"#;
        let result = JSONTools::new()
            .flatten()
            .key_replacement("r'(User|Admin|Guest)_'", "")
            .handle_key_collision(true)
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        // Should collect mixed types into an array (order may vary)
        if let Some(array) = parsed["name"].as_array() {
            assert_eq!(array.len(), 3);

            // Check that we have all expected values
            let has_john = array.iter().any(|v| v.as_str() == Some("John"));
            let has_42 = array.iter().any(|v| v.as_i64() == Some(42));
            let has_true = array.iter().any(|v| v.as_bool() == Some(true));

            assert!(has_john);
            assert!(has_42);
            assert!(has_true);
        } else {
            panic!("Expected array for 'name' key");
        }
    }

    #[test]
    fn test_collision_with_filtering() {
        let json = r#"{"User_name": "John", "Admin_name": "", "Guest_name": "Bob"}"#;
        let result = JSONTools::new()
            .flatten()
            .key_replacement("r'(User|Admin|Guest)_'", "")
            .remove_empty_strings(true)
            .handle_key_collision(true)
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        // Collision handling now properly filters out empty values during array creation
        if let Some(array) = parsed["name"].as_array() {
            // The array should only contain non-empty values after filtering
            assert_eq!(array.len(), 2);
            let values: Vec<&str> = array.iter().map(|v| v.as_str().unwrap()).collect();
            assert!(values.contains(&"John"));
            assert!(values.contains(&"Bob"));
            // Empty string should be filtered out during collision handling
        } else {
            panic!("Expected array for 'name' key");
        }
    }

    // ===== TYPE CONVERSION TESTS =====

    #[test]
    fn test_basic_number_conversion() {
        let json = r#"{"id": "123", "price": "45.67", "count": "-10"}"#;
        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        assert_eq!(parsed["id"], 123);
        assert_eq!(parsed["price"], 45.67);
        assert_eq!(parsed["count"], -10);
    }

    /// Regression test for `canonical_json_integer`'s fast path in convert.rs:
    /// already-clean integer strings ("123", "-45", "0") must convert identically
    /// to how the (slower) float round-trip path would have converted them.
    #[test]
    fn test_clean_integer_fast_path() {
        let json = r#"{"a": "123", "b": "-45", "c": "0", "d": "9007199254740993"}"#;
        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        assert_eq!(parsed["a"], 123);
        assert_eq!(parsed["b"], -45);
        assert_eq!(parsed["c"], 0);
        // 16 digits: within the fast path's 18-digit bound, but big enough that an
        // f64 round-trip would lose precision -- confirms the fast path preserves
        // the exact original digits rather than reformatting through a float.
        assert_eq!(parsed["d"], 9007199254740993i64);
    }

    /// Leading zeros ("007") are not valid unquoted JSON number syntax, so they
    /// must never take the fast path -- must still go through the existing
    /// float round-trip, which normalizes to "7" (matches pre-existing behavior).
    #[test]
    fn test_leading_zero_not_fast_pathed() {
        let json = r#"{"code": "007"}"#;
        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        assert_eq!(parsed["code"], 7);
    }

    /// "-0" must keep converting to "0" (sign dropped), matching the existing
    /// float round-trip's behavior (`-0.0f64 as i64 == 0`) -- the fast path
    /// deliberately excludes "-0" to avoid silently changing this.
    #[test]
    fn test_negative_zero_matches_existing_behavior() {
        let json = r#"{"value": "-0"}"#;
        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        assert_eq!(parsed["value"], 0);
        assert!(!flattened.contains("-0"));
    }

    /// Integers too large for even u64 (>20 digits) fall through to the
    /// pre-existing float round-trip path unchanged -- which, since the value
    /// is unrepresentable exactly in an i64/u64 either way, formats it as a
    /// (lossy, scientific-notation) float rather than leaving it as a string.
    /// This isn't behavior the fast path introduces; it documents the existing
    /// fallback so a future change to it doesn't silently regress unnoticed.
    #[test]
    fn test_integer_beyond_u64_falls_through_to_float() {
        let json = r#"{"huge": "99999999999999999999999999"}"#;
        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        assert!(parsed["huge"].is_number());
        assert_ne!(
            parsed["huge"],
            serde_json::json!("99999999999999999999999999")
        );
    }

    /// Correctness regression test: before `canonical_json_integer`, `auto_convert_types`
    /// silently corrupted the trailing digits of exact 64-bit-range integer strings by
    /// routing them through `f64` (only ~15-17 significant decimal digits of exact
    /// precision) before reformatting. Real-world 64-bit IDs (Snowflake/Discord/database
    /// bigint IDs, commonly stored as JSON strings *specifically* to avoid this exact
    /// class of precision loss elsewhere) are typically 17-19 digits, so this was a live
    /// bug, not a hypothetical one. Confirmed via byte-for-byte A/B comparison against the
    /// pre-fix implementation: every one of these previously came out corrupted.
    #[test]
    fn test_large_integer_precision_exact_at_boundaries() {
        let json = r#"{
            "a": "999999999999999999",
            "b": "12345678901234567",
            "c": "123456789012345678",
            "d": "1234567890123456789",
            "e": "9223372036854775807",
            "f": "9223372036854775809",
            "g": "-9223372036854775807",
            "h": "-9223372036854775808",
            "i": "18446744073709551614",
            "j": "99999999999999999"
        }"#;
        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        assert_eq!(parsed["a"], 999999999999999999i64);
        assert_eq!(parsed["b"], 12345678901234567i64);
        assert_eq!(parsed["c"], 123456789012345678i64);
        assert_eq!(parsed["d"], 1234567890123456789i64);
        assert_eq!(parsed["e"], i64::MAX);
        assert_eq!(parsed["f"], 9223372036854775809u64); // i64::MAX + 2, fits u64
        assert_eq!(parsed["g"], -9223372036854775807i64); // i64::MIN + 1
        assert_eq!(parsed["h"], i64::MIN);
        assert_eq!(parsed["i"], 18446744073709551614u64); // u64::MAX - 1
        assert_eq!(parsed["j"], 99999999999999999i64);
    }

    /// 20-digit negative numbers (magnitude beyond i64::MIN) and >20-digit
    /// positive numbers (beyond u64::MAX) cannot be exactly represented by
    /// either i64 or u64, so the fast path must decline them and leave the
    /// existing (lossy but pre-existing) fallback behavior untouched.
    #[test]
    fn test_integers_beyond_i64_u64_range_unchanged() {
        let json = r#"{"neg": "-18446744073709551615", "pos": "999999999999999999999"}"#;
        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        // Both are converted (existing fallback always produces *some* numeric
        // output for finite parseable values) but not preserved exactly --
        // this documents the pre-existing behavior, unaffected by the fast path.
        assert!(parsed["neg"].is_number());
        assert!(parsed["pos"].is_number());
    }

    #[test]
    fn test_thousands_separator_us_format() {
        let json = r#"{"amount": "1,234.56", "total": "1,000,000"}"#;
        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        assert_eq!(parsed["amount"], 1234.56);
        assert_eq!(parsed["total"], 1000000);
    }

    #[test]
    fn test_thousands_separator_european_format() {
        let json = r#"{"amount": "1.234,56", "total": "1.000.000,00"}"#;
        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        assert_eq!(parsed["amount"], 1234.56);
        assert_eq!(parsed["total"], 1000000.0);
    }

    #[test]
    fn test_currency_symbols() {
        let json = r#"{"usd": "$123.45", "eur": "€99.99", "gbp": "£50.00"}"#;
        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        assert_eq!(parsed["usd"], 123.45);
        assert_eq!(parsed["eur"], 99.99);
        assert_eq!(parsed["gbp"], 50.0);
    }

    /// Regression test for `strip_trailing_ascii_pair` in convert.rs: credit/debit
    /// suffix stripping must match `trim_end_matches`'s exact chained semantics --
    /// each of CR/DR/cr/dr is stripped exhaustively before the next is tried, so
    /// mixed-suffix strings like "100CRDR"/"100DRCR" resolve asymmetrically (order
    /// matters: only a trailing "DR" gets caught by the first pass in "100CRDR",
    /// leaving "CR" behind and making it fail to parse as a number at all).
    #[test]
    fn test_credit_debit_suffix_stripping() {
        let json = r#"{
            "a": "100CR", "b": "100DR", "c": "100cr", "d": "100dr",
            "e": "100CRDR", "f": "100DRCR", "g": "100crdr", "h": "100drcr"
        }"#;
        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        assert_eq!(parsed["a"], 100);
        assert_eq!(parsed["b"], 100);
        assert_eq!(parsed["c"], 100);
        assert_eq!(parsed["d"], 100);
        // Asymmetric: "CR" isn't a suffix of "100CRDR" (it ends in "DR"), so only the
        // "DR" pass strips anything, leaving "100CR" -- not a valid number, so the
        // original string is kept unconverted.
        assert_eq!(parsed["e"], "100CRDR");
        assert_eq!(parsed["f"], 100);
        assert_eq!(parsed["g"], "100crdr");
        assert_eq!(parsed["h"], 100);
    }

    #[test]
    fn test_scientific_notation() {
        let json = r#"{"small": "1.23e-4", "large": "1e5", "negative": "-2.5e3"}"#;
        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        assert_eq!(parsed["small"], 0.000123);
        assert_eq!(parsed["large"], 100000.0);
        assert_eq!(parsed["negative"], -2500.0);
    }

    #[test]
    fn test_boolean_conversion() {
        let json =
            r#"{"a": "true", "b": "TRUE", "c": "True", "d": "false", "e": "FALSE", "f": "False"}"#;
        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        assert_eq!(parsed["a"], true);
        assert_eq!(parsed["b"], true);
        assert_eq!(parsed["c"], true);
        assert_eq!(parsed["d"], false);
        assert_eq!(parsed["e"], false);
        assert_eq!(parsed["f"], false);
    }

    #[test]
    fn test_keep_invalid_strings() {
        let json = r#"{"name": "John", "code": "ABC123", "maybe": "yes", "invalid": "12.34.56", "text": "hello123"}"#;
        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        assert_eq!(parsed["name"], "John");
        assert_eq!(parsed["code"], "ABC123"); // Not a valid number (mixed text and digits)
        assert_eq!(parsed["maybe"], true); // "yes" is now a valid boolean
        assert_eq!(parsed["invalid"], "12.34.56"); // Invalid number (multiple decimal points)
        assert_eq!(parsed["text"], "hello123"); // Text with numbers stays as string
    }

    #[test]
    fn test_mixed_conversion() {
        let json = r#"{"id": "123", "name": "Alice", "price": "$1,234.56", "active": "true", "code": "XYZ"}"#;
        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        assert_eq!(parsed["id"], 123);
        assert_eq!(parsed["name"], "Alice");
        assert_eq!(parsed["price"], 1234.56);
        assert_eq!(parsed["active"], true);
        assert_eq!(parsed["code"], "XYZ");
    }

    #[test]
    fn test_nested_conversion() {
        let json = r#"{"user": {"id": "456", "age": "25", "verified": "true"}}"#;
        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        assert_eq!(parsed["user.id"], 456);
        assert_eq!(parsed["user.age"], 25);
        assert_eq!(parsed["user.verified"], true);
    }

    #[test]
    fn test_array_conversion() {
        let json = r#"{"numbers": ["123", "45.6", "true", "invalid"]}"#;
        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        assert_eq!(parsed["numbers.0"], 123);
        assert_eq!(parsed["numbers.1"], 45.6);
        assert_eq!(parsed["numbers.2"], true);
        assert_eq!(parsed["numbers.3"], "invalid");
    }

    #[test]
    fn test_conversion_disabled_by_default() {
        let json = r#"{"id": "123", "active": "true"}"#;
        let result = JSONTools::new().flatten().execute(json).unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        // Should keep as strings when conversion is disabled
        assert_eq!(parsed["id"], "123");
        assert_eq!(parsed["active"], "true");
    }

    #[test]
    fn test_unflatten_with_conversion() {
        let json = r#"{"user.id": "789", "user.active": "false"}"#;
        let result = JSONTools::new()
            .unflatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();
        let unflattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&unflattened).unwrap();

        assert_eq!(parsed["user"]["id"], 789);
        assert_eq!(parsed["user"]["active"], false);
    }

    #[test]
    fn test_normal_mode_with_conversion() {
        let json = r#"{"user": {"id": "999", "enabled": "TRUE"}}"#;
        let result = JSONTools::new()
            .normal()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();
        let processed = extract_single(result);
        let parsed: Value = serde_json::from_str(&processed).unwrap();

        assert_eq!(parsed["user"]["id"], 999);
        assert_eq!(parsed["user"]["enabled"], true);
    }

    #[test]
    fn test_normal_mode_collision_handling() {
        // Key replacement that creates duplicate keys, verifying array merging
        let json = r#"{"user_name": "Alice", "admin_name": "Bob"}"#;
        let result = JSONTools::new()
            .normal()
            .key_replacement("user_", "")
            .key_replacement("admin_", "")
            .handle_key_collision(true)
            .execute(json)
            .unwrap();
        let processed = extract_single(result);
        let parsed: Value = serde_json::from_str(&processed).unwrap();

        // Both keys become "name", should be merged into array
        assert!(parsed["name"].is_array());
        let names: Vec<&str> = parsed["name"]
            .as_array()
            .unwrap()
            .iter()
            .map(|v| v.as_str().unwrap())
            .collect();
        assert!(names.contains(&"Alice"));
        assert!(names.contains(&"Bob"));
    }

    #[test]
    fn test_normal_mode_collision_handling_no_actual_collisions() {
        // handle_key_collision(true) alone (no key replacements, already-unique
        // keys at every nesting depth) should leave the document completely
        // unaffected -- guards SlowObjectEntry's String -> Cow<'a, str> refactor
        // on its "key unchanged" path (the common case).
        let json = r#"{"a": 1, "nested": {"b": 2, "deeper": {"c": 3, "d": 4}}, "e": 5}"#;
        let result = JSONTools::new()
            .normal()
            .handle_key_collision(true)
            .execute(json)
            .unwrap();
        let processed = extract_single(result);
        let parsed: Value = serde_json::from_str(&processed).unwrap();

        assert_eq!(parsed["a"], 1);
        assert_eq!(parsed["nested"]["b"], 2);
        assert_eq!(parsed["nested"]["deeper"]["c"], 3);
        assert_eq!(parsed["nested"]["deeper"]["d"], 4);
        assert_eq!(parsed["e"], 5);
        // None of these should have been wrapped into collision arrays
        assert!(!parsed["a"].is_array());
        assert!(!parsed["nested"]["b"].is_array());
    }

    #[test]
    fn test_normal_mode_collision_handling_nested_object() {
        // Collisions inside a NESTED object, not just top-level -- NormalSlowWalker
        // recurses into every object, so this guards serialize_with_collisions's
        // ordered/key_positions rewrite at a nesting depth beyond the root.
        let json = r#"{"outer": {"user_name": "Alice", "admin_name": "Bob", "id": 1}}"#;
        let result = JSONTools::new()
            .normal()
            .key_replacement("user_", "")
            .key_replacement("admin_", "")
            .handle_key_collision(true)
            .execute(json)
            .unwrap();
        let processed = extract_single(result);
        let parsed: Value = serde_json::from_str(&processed).unwrap();

        assert!(parsed["outer"]["name"].is_array());
        let names: Vec<&str> = parsed["outer"]["name"]
            .as_array()
            .unwrap()
            .iter()
            .map(|v| v.as_str().unwrap())
            .collect();
        assert!(names.contains(&"Alice"));
        assert!(names.contains(&"Bob"));
        assert_eq!(parsed["outer"]["id"], 1);
    }

    #[test]
    fn test_normal_mode_deep_nesting_with_filtering() {
        // Build 50+ levels of nesting with a mix of filterable and retained values
        let inner = r#"{"a":{"b":{"keep":"hello","remove":"","null_val":null}}}"#;
        let mut json = inner.to_string();
        for i in 0..50 {
            json = format!(r#"{{"level{}": {}}}"#, i, json);
        }

        let result = JSONTools::new()
            .normal()
            .remove_empty_strings(true)
            .remove_nulls(true)
            .execute(&json)
            .unwrap();
        let processed = extract_single(result);
        let parsed: Value = serde_json::from_str(&processed).unwrap();

        // Navigate to the deepest level
        let mut current = &parsed;
        for i in (0..50).rev() {
            let key = format!("level{}", i);
            assert!(current[&key].is_object(), "missing level{}", i);
            current = &current[&key];
        }
        // "keep" should survive, "remove" and "null_val" should be filtered
        assert_eq!(current["a"]["b"]["keep"], "hello");
        assert_eq!(current["a"]["b"]["remove"], Value::Null); // filtered = absent = Null in serde
        assert_eq!(current["a"]["b"]["null_val"], Value::Null); // filtered
    }

    #[test]
    fn test_normal_mode_unicode_keys_with_lowercase() {
        // Normal mode slow walker uses .to_lowercase() (full Unicode lowercasing)
        let json = r#"{"Ñoño": 1, "ÜBER": 2, "Hello": 3, "café": 4}"#;
        let result = JSONTools::new()
            .normal()
            .lowercase_keys(true)
            .execute(json)
            .unwrap();
        let processed = extract_single(result);
        let parsed: Value = serde_json::from_str(&processed).unwrap();

        // ASCII uppercase converted: "Hello" -> "hello"
        assert_eq!(parsed["hello"], 3);
        // Full Unicode lowercasing: Ñ -> ñ
        assert_eq!(parsed["ñoño"], 1);
        // Full Unicode lowercasing: Ü -> ü
        assert_eq!(parsed["über"], 2);
        // Already lowercase stays unchanged
        assert_eq!(parsed["café"], 4);
    }
}

// ===== MEMORY PROFILING TESTS =====

#[cfg(test)]
mod memory_profiling_tests {
    use crate::tests::{extract_multiple, extract_single};
    use crate::JSONTools;
    use serde_json::Value;

    #[test]
    fn test_parallel_memory_overhead() {
        // Create a batch of 100 JSON documents
        let json_docs: Vec<String> = (0..100)
            .map(|i| {
                format!(
                    r#"{{"id": {}, "name": "User {}", "email": "user{}@example.com", "age": {}, "active": true}}"#,
                    i, i, i, 20 + (i % 50)
                )
            })
            .collect();

        let json_refs: Vec<&str> = json_docs.iter().map(|s| s.as_str()).collect();

        // Test sequential processing
        let result_seq = JSONTools::new()
            .flatten()
            .parallel_threshold(usize::MAX) // Force sequential
            .execute(json_refs.clone())
            .expect("Sequential processing failed");

        // Test parallel processing
        let result_par = JSONTools::new()
            .flatten()
            .parallel_threshold(1) // Force parallel
            .execute(json_refs)
            .expect("Parallel processing failed");

        // Both should produce identical results - compare the actual strings
        let (seq_results, par_results) = match (result_seq, result_par) {
            (crate::JsonOutput::Multiple(seq), crate::JsonOutput::Multiple(par)) => (seq, par),
            _ => panic!("Expected Multiple output"),
        };

        assert_eq!(
            seq_results.len(),
            par_results.len(),
            "Result counts should match"
        );
        for (i, (seq, par)) in seq_results.iter().zip(par_results.iter()).enumerate() {
            assert_eq!(seq, par, "Result {} should be identical", i);
        }

        // Validate: results should be reasonable size
        let total_size: usize = seq_results.iter().map(|s| s.len()).sum();
        let avg_size = total_size / seq_results.len();

        println!("Average result size: {} bytes", avg_size);
        println!(
            "Total results size: {} bytes ({:.2} KB)",
            total_size,
            total_size as f64 / 1024.0
        );

        // Each flattened JSON should be reasonable (< 1KB for this test data)
        assert!(avg_size < 1000, "Average result size is unexpectedly large");
    }

    #[test]
    fn test_effective_thread_count_respects_override() {
        // Regression test: `num_threads` was previously stored/validated but never
        // consulted by the parallel dispatch paths, which always used
        // available_parallelism() regardless of the configured override.
        let with_override = crate::ProcessingConfig {
            num_threads: Some(2),
            ..crate::ProcessingConfig::new()
        };
        assert_eq!(with_override.effective_thread_count(1000), 2);

        // Override is still capped by the item count.
        assert_eq!(with_override.effective_thread_count(1), 1);

        // 0 is rejected by the builder before reaching here (see JSONTools::num_threads
        // validation), but effective_thread_count defends against it anyway.
        let zero_override = crate::ProcessingConfig {
            num_threads: Some(0),
            ..crate::ProcessingConfig::new()
        };
        assert_eq!(zero_override.effective_thread_count(1000), 1);

        // None falls back to available_parallelism(), capped by item count.
        let default_config = crate::ProcessingConfig::new();
        let n = default_config.effective_thread_count(1000);
        assert!(n >= 1);
        assert_eq!(default_config.effective_thread_count(1), 1);
    }

    #[test]
    fn test_num_threads_builder_option_produces_correct_batch_results() {
        // End-to-end check that constraining num_threads still yields correct,
        // order-preserving batch output through the parallel dispatch path.
        let json_docs: Vec<String> = (0..50)
            .map(|i| format!(r#"{{"id": {i}, "nested": {{"value": {i}}}}}"#))
            .collect();
        let json_refs: Vec<&str> = json_docs.iter().map(|s| s.as_str()).collect();

        let result = JSONTools::new()
            .flatten()
            .parallel_threshold(1) // force the parallel path
            .num_threads(Some(2))
            .execute(json_refs)
            .expect("Batch processing with constrained num_threads failed");

        let results = extract_multiple(result);
        assert_eq!(results.len(), 50);
        for (i, flat) in results.iter().enumerate() {
            let parsed: Value = serde_json::from_str(flat).unwrap();
            assert_eq!(parsed["id"], i);
            assert_eq!(parsed["nested.value"], i);
        }
    }

    #[test]
    fn test_num_threads_batch_with_nested_parallel_documents() {
        // Round 16: a batch of documents individually wide enough to also trigger
        // per-document nested parallelism (flatten_collecting_parallel), combined
        // with a `num_threads(Some(n))` override and a low parallel_threshold, so
        // this exercises both batch-level AND nested-per-document parallel dispatch
        // at once -- the exact shape that caused flatten_collecting_parallel to
        // rebuild a redundant thread pool per document before the round-16 fix.
        // Guards correctness (not just speed): the fix only changes which pool runs
        // the work, never what gets computed.
        let json_docs: Vec<String> = (0..20)
            .map(|doc_i| {
                let fields: Vec<String> = (0..150)
                    .map(|k| format!(r#""field_{k}": {}"#, doc_i * 1000 + k))
                    .collect();
                format!("{{{}}}", fields.join(","))
            })
            .collect();
        let json_refs: Vec<&str> = json_docs.iter().map(|s| s.as_str()).collect();

        let result = JSONTools::new()
            .flatten()
            .parallel_threshold(1)
            .nested_parallel_threshold(50)
            .num_threads(Some(4))
            .execute(json_refs)
            .expect("Batch with nested-parallel documents failed");

        let results = extract_multiple(result);
        assert_eq!(results.len(), 20);
        for (doc_i, flat) in results.iter().enumerate() {
            let parsed: Value = serde_json::from_str(flat).unwrap();
            assert_eq!(parsed.as_object().unwrap().len(), 150);
            for k in 0..150 {
                assert_eq!(parsed[format!("field_{k}")], doc_i * 1000 + k);
            }
        }
    }

    #[test]
    fn test_num_threads_single_wide_document_still_correct() {
        // The non-batch path: a single document (not a Vec/list input) wide enough
        // to trigger nested parallelism, with num_threads(Some(n)) set. No ambient
        // batch-level pool exists here, so flatten_collecting_parallel must still
        // build its own dedicated pool (current_num_threads() won't match n) --
        // guards that the round-16 fix's new branch doesn't accidentally skip pool
        // construction when one is actually needed.
        let fields: Vec<String> = (0..150).map(|k| format!(r#""field_{k}": {k}"#)).collect();
        let json = format!("{{{}}}", fields.join(","));

        let result = JSONTools::new()
            .flatten()
            .nested_parallel_threshold(50)
            .num_threads(Some(3))
            .execute(json.as_str())
            .expect("Single wide document with num_threads failed");

        let flat = extract_single(result);
        let parsed: Value = serde_json::from_str(&flat).unwrap();
        assert_eq!(parsed.as_object().unwrap().len(), 150);
        for k in 0..150 {
            assert_eq!(parsed[format!("field_{k}")], k);
        }
    }

    #[test]
    fn test_large_batch_memory_scaling() {
        // Test that memory scales linearly with batch size, not exponentially
        let batch_sizes = vec![10, 50, 100, 500];
        let mut bytes_per_item = Vec::new();

        for &size in &batch_sizes {
            let json_docs: Vec<String> = (0..size)
                .map(|i| {
                    format!(
                        r#"{{"id": {}, "data": "Item {}", "value": {}}}"#,
                        i,
                        i,
                        i * 100
                    )
                })
                .collect();

            let json_refs: Vec<&str> = json_docs.iter().map(|s| s.as_str()).collect();

            let result = JSONTools::new()
                .flatten()
                .parallel_threshold(10)
                .execute(json_refs)
                .expect("Processing failed");

            // Measure output size as proxy for memory usage
            if let crate::JsonOutput::Multiple(results) = result {
                let total_bytes: usize = results
                    .iter()
                    .map(|s| s.len() + std::mem::size_of::<String>())
                    .sum();
                let per_item = total_bytes / size;
                bytes_per_item.push(per_item);

                println!(
                    "Batch size {}: {} bytes total, {} bytes per item",
                    size, total_bytes, per_item
                );
            }
        }

        // Validate: per-item memory should be relatively constant (within 2x)
        let min_per_item = *bytes_per_item.iter().min().unwrap();
        let max_per_item = *bytes_per_item.iter().max().unwrap();
        let ratio = max_per_item as f64 / min_per_item as f64;

        println!("Memory per item ratio (max/min): {:.2}x", ratio);

        // Linear scaling means ratio should be close to 1.0
        // Allow up to 2x variation due to Vec overhead and small batch effects
        assert!(
            ratio < 2.0,
            "Memory per item varies too much ({:.2}x), suggesting non-linear scaling",
            ratio
        );
    }

    #[test]
    fn test_chunked_processing_memory() {
        // Test that chunked processing (>1000 items) doesn't increase memory per item
        let size = 1500; // Triggers chunked processing

        let json_docs: Vec<String> = (0..size)
            .map(|i| format!(r#"{{"id": {}, "value": {}}}"#, i, i * 10))
            .collect();

        let json_refs: Vec<&str> = json_docs.iter().map(|s| s.as_str()).collect();

        let result = JSONTools::new()
            .flatten()
            .parallel_threshold(10)
            .execute(json_refs)
            .expect("Chunked processing failed");

        // Measure output size
        if let crate::JsonOutput::Multiple(results) = result {
            assert_eq!(results.len(), size, "Should process all items");

            let total_bytes: usize = results
                .iter()
                .map(|s| s.len() + std::mem::size_of::<String>())
                .sum();
            let per_item = total_bytes / size;

            println!(
                "Chunked processing (1500 items): {} bytes total, {} bytes per item",
                total_bytes, per_item
            );

            // Validate: per-item memory should be reasonable (< 1KB per item for this simple JSON)
            assert!(
                per_item < 1000,
                "Per-item memory ({} bytes) is too high for chunked processing",
                per_item
            );
        }
    }

    #[test]
    fn test_memory_cleanup_after_processing() {
        // Test that results can be properly dropped and don't hold excessive memory
        let json_docs: Vec<String> = (0..100)
            .map(|i| format!(r#"{{"id": {}, "data": "test"}}"#, i))
            .collect();

        let json_refs: Vec<&str> = json_docs.iter().map(|s| s.as_str()).collect();

        let result = JSONTools::new()
            .flatten()
            .parallel_threshold(10)
            .execute(json_refs)
            .expect("Processing failed");

        // Validate result structure
        if let crate::JsonOutput::Multiple(results) = result {
            assert_eq!(results.len(), 100, "Should have 100 results");

            // Each result should be a valid JSON string
            for (i, result_str) in results.iter().enumerate() {
                assert!(
                    result_str.contains("id"),
                    "Result {} should contain 'id' field",
                    i
                );
                assert!(
                    result_str.contains("data"),
                    "Result {} should contain 'data' field",
                    i
                );
            }

            println!("Successfully processed and validated 100 items");
            println!("Results can be dropped without issues");
        }
    }

    #[test]
    fn test_parallel_vs_sequential_same_output_size() {
        // Verify that parallel and sequential produce identical output sizes
        let json_docs: Vec<String> = (0..200)
            .map(|i| {
                format!(
                    r#"{{"id": {}, "nested": {{"value": {}, "name": "Item {}"}}}}"#,
                    i,
                    i * 10,
                    i
                )
            })
            .collect();

        let json_refs: Vec<&str> = json_docs.iter().map(|s| s.as_str()).collect();

        // Sequential
        let result_seq = JSONTools::new()
            .flatten()
            .parallel_threshold(usize::MAX)
            .execute(json_refs.clone())
            .expect("Sequential failed");

        // Parallel
        let result_par = JSONTools::new()
            .flatten()
            .parallel_threshold(1)
            .execute(json_refs)
            .expect("Parallel failed");

        // Extract results
        let (seq, par) = match (result_seq, result_par) {
            (crate::JsonOutput::Multiple(seq), crate::JsonOutput::Multiple(par)) => (seq, par),
            _ => panic!("Expected Multiple output"),
        };

        // Both should produce identical results
        assert_eq!(seq.len(), par.len(), "Result counts should match");
        for (i, (s, p)) in seq.iter().zip(par.iter()).enumerate() {
            assert_eq!(s, p, "Result {} should be identical", i);
        }

        // Measure sizes
        let seq_size: usize = seq.iter().map(|s| s.len()).sum();
        let par_size: usize = par.iter().map(|s| s.len()).sum();

        println!("Sequential total size: {} bytes", seq_size);
        println!("Parallel total size: {} bytes", par_size);

        assert_eq!(seq_size, par_size, "Output sizes should be identical");
    }
}

// ===== NESTED PARALLELISM TESTS =====

#[cfg(test)]
mod nested_parallelism_tests {
    use crate::{JSONTools, JsonOutput};

    /// Test that nested parallelism produces the same results as sequential processing
    #[test]
    fn test_nested_parallel_consistency() {
        // Create a large nested JSON document
        let json = r#"{
            "users": [
                {"id": 1, "name": "Alice", "tags": ["admin", "user"]},
                {"id": 2, "name": "Bob", "tags": ["user"]},
                {"id": 3, "name": "Charlie", "tags": ["moderator", "user"]},
                {"id": 4, "name": "David", "tags": ["user"]},
                {"id": 5, "name": "Eve", "tags": ["admin", "moderator"]}
            ],
            "settings": {
                "theme": "dark",
                "notifications": {
                    "email": true,
                    "push": false,
                    "sms": true
                },
                "privacy": {
                    "profile_visible": true,
                    "show_email": false
                }
            },
            "metadata": {
                "version": "1.0",
                "created": "2024-01-01",
                "updated": "2024-01-15"
            }
        }"#;

        // Flatten with sequential processing (nested_threshold = usize::MAX)
        let sequential_result = JSONTools::new()
            .flatten()
            .nested_parallel_threshold(usize::MAX)
            .execute(json)
            .expect("Sequential flatten failed");

        // Flatten with nested parallelism (nested_threshold = 2)
        let parallel_result = JSONTools::new()
            .flatten()
            .nested_parallel_threshold(2)
            .execute(json)
            .expect("Parallel flatten failed");

        // Extract the JSON strings for comparison
        let sequential_json = match sequential_result {
            JsonOutput::Single(s) => s,
            _ => panic!("Expected single output"),
        };

        let parallel_json = match parallel_result {
            JsonOutput::Single(s) => s,
            _ => panic!("Expected single output"),
        };

        // Parse both results to compare as JSON objects (order-independent)
        let sequential_value: serde_json::Value =
            serde_json::from_str(&sequential_json).expect("Failed to parse sequential result");
        let parallel_value: serde_json::Value =
            serde_json::from_str(&parallel_json).expect("Failed to parse parallel result");

        assert_eq!(
            sequential_value, parallel_value,
            "Nested parallel processing should produce identical results to sequential processing"
        );
    }

    /// Test nested parallelism with large objects
    #[test]
    fn test_large_object_nested_parallelism() {
        // Create a JSON object with 150 keys (exceeds default threshold of 100)
        let mut json = String::from("{");
        for i in 0..150 {
            if i > 0 {
                json.push(',');
            }
            json.push_str(&format!(
                r#""key_{}": {{"nested": "value_{}", "id": {}}}"#,
                i, i, i
            ));
        }
        json.push('}');

        // Flatten with sequential processing
        let sequential_result = JSONTools::new()
            .flatten()
            .nested_parallel_threshold(usize::MAX)
            .execute(&json)
            .expect("Sequential flatten failed");

        // Flatten with nested parallelism (threshold = 100)
        let parallel_result = JSONTools::new()
            .flatten()
            .nested_parallel_threshold(100)
            .execute(&json)
            .expect("Parallel flatten failed");

        // Extract and compare
        let sequential_json = match sequential_result {
            JsonOutput::Single(s) => s,
            _ => panic!("Expected single output"),
        };

        let parallel_json = match parallel_result {
            JsonOutput::Single(s) => s,
            _ => panic!("Expected single output"),
        };

        let sequential_value: serde_json::Value = serde_json::from_str(&sequential_json).unwrap();
        let parallel_value: serde_json::Value = serde_json::from_str(&parallel_json).unwrap();

        assert_eq!(sequential_value, parallel_value);
    }

    /// Test nested parallelism with large arrays
    #[test]
    fn test_large_array_nested_parallelism() {
        // Create a JSON array with 150 items (exceeds default threshold of 100)
        let mut json = String::from("[");
        for i in 0..150 {
            if i > 0 {
                json.push(',');
            }
            json.push_str(&format!(
                r#"{{"id": {}, "value": "item_{}", "nested": {{"data": "test_{}"}} }}"#,
                i, i, i
            ));
        }
        json.push(']');

        // Flatten with sequential processing
        let sequential_result = JSONTools::new()
            .flatten()
            .nested_parallel_threshold(usize::MAX)
            .execute(&json)
            .expect("Sequential flatten failed");

        // Flatten with nested parallelism (threshold = 100)
        let parallel_result = JSONTools::new()
            .flatten()
            .nested_parallel_threshold(100)
            .execute(&json)
            .expect("Parallel flatten failed");

        // Extract and compare
        let sequential_json = match sequential_result {
            JsonOutput::Single(s) => s,
            _ => panic!("Expected single output"),
        };

        let parallel_json = match parallel_result {
            JsonOutput::Single(s) => s,
            _ => panic!("Expected single output"),
        };

        let sequential_value: serde_json::Value = serde_json::from_str(&sequential_json).unwrap();
        let parallel_value: serde_json::Value = serde_json::from_str(&parallel_json).unwrap();

        assert_eq!(sequential_value, parallel_value);
    }

    /// Test that small objects/arrays stay sequential
    #[test]
    fn test_small_structures_stay_sequential() {
        let json = r#"{
            "small_object": {"a": 1, "b": 2, "c": 3},
            "small_array": [1, 2, 3, 4, 5]
        }"#;

        // This should work fine even with a very low threshold
        // because the structures are small
        let result = JSONTools::new()
            .flatten()
            .nested_parallel_threshold(10)
            .execute(json)
            .expect("Flatten failed");

        match result {
            JsonOutput::Single(s) => {
                let value: serde_json::Value = serde_json::from_str(&s).unwrap();
                assert!(value.is_object());
            }
            _ => panic!("Expected single output"),
        }
    }

    /// Test environment variable configuration
    #[test]
    fn test_environment_variable_nested_threshold() {
        std::env::set_var("JSON_TOOLS_NESTED_PARALLEL_THRESHOLD", "50");

        let tools = JSONTools::new();

        // The default should now be 50 from the environment variable
        // We can't directly access the field, but we can test that it works
        let json = r#"{"test": "value"}"#;
        let result = tools.flatten().execute(json);

        assert!(result.is_ok());

        std::env::remove_var("JSON_TOOLS_NESTED_PARALLEL_THRESHOLD");
    }

    /// Test deeply nested structures with parallelism
    #[test]
    fn test_deeply_nested_parallelism() {
        // Create a deeply nested structure with wide branches
        let json = r#"{
            "level1": {
                "items": [
                    {"id": 1, "data": {"values": [1, 2, 3, 4, 5]}},
                    {"id": 2, "data": {"values": [6, 7, 8, 9, 10]}},
                    {"id": 3, "data": {"values": [11, 12, 13, 14, 15]}}
                ],
                "metadata": {
                    "created": "2024-01-01",
                    "tags": ["a", "b", "c", "d", "e"]
                }
            }
        }"#;

        let sequential_result = JSONTools::new()
            .flatten()
            .nested_parallel_threshold(usize::MAX)
            .execute(json)
            .expect("Sequential flatten failed");

        let parallel_result = JSONTools::new()
            .flatten()
            .nested_parallel_threshold(2)
            .execute(json)
            .expect("Parallel flatten failed");

        let sequential_json = match sequential_result {
            JsonOutput::Single(s) => s,
            _ => panic!("Expected single output"),
        };

        let parallel_json = match parallel_result {
            JsonOutput::Single(s) => s,
            _ => panic!("Expected single output"),
        };

        let sequential_value: serde_json::Value = serde_json::from_str(&sequential_json).unwrap();
        let parallel_value: serde_json::Value = serde_json::from_str(&parallel_json).unwrap();

        assert_eq!(sequential_value, parallel_value);
    }
}

// ===== PARALLEL REGEX CACHE TESTS =====

#[cfg(test)]
mod parallel_regex_cache_tests {
    use super::extract_single;
    use crate::{JSONTools, JsonOutput};
    use serde_json::Value;

    /// Test that parallel processing with regex replacements works correctly
    #[test]
    fn test_parallel_processing_with_regex_replacements() {
        // Create a batch of JSON documents with patterns to replace
        let json_docs: Vec<String> = (0..100)
            .map(|i| {
                format!(
                    r#"{{"user_id": {}, "admin_name": "Admin{}", "guest_email": "guest{}@example.com"}}"#,
                    i, i, i
                )
            })
            .collect();

        let json_refs: Vec<&str> = json_docs.iter().map(|s| s.as_str()).collect();

        // Process with parallel threshold = 10 (should use parallel processing)
        let result = JSONTools::new()
            .flatten()
            .key_replacement("r'(user|admin|guest)_'", "")
            .value_replacement("r'@example\\.com'", "@company.org")
            .parallel_threshold(10)
            .execute(json_refs)
            .expect("Parallel processing failed");

        // Verify results
        if let JsonOutput::Multiple(results) = result {
            assert_eq!(results.len(), 100);

            for (i, result_str) in results.iter().enumerate() {
                let value: serde_json::Value =
                    serde_json::from_str(result_str).expect("Failed to parse result");

                // Check that key replacements worked
                assert!(
                    value.as_object().unwrap().contains_key("id"),
                    "Should have 'id' key"
                );
                assert!(
                    value.as_object().unwrap().contains_key("name"),
                    "Should have 'name' key"
                );
                assert!(
                    value.as_object().unwrap().contains_key("email"),
                    "Should have 'email' key"
                );

                // Check that value replacements worked
                let email = value["email"].as_str().unwrap();
                assert!(
                    email.contains("@company.org"),
                    "Email should be replaced: {} (item {})",
                    email,
                    i
                );
            }
        } else {
            panic!("Expected Multiple output");
        }
    }

    /// Test that parallel and sequential produce identical results with regex
    #[test]
    fn test_parallel_vs_sequential_consistency() {
        let json_docs: Vec<String> = (0..50)
            .map(|i| {
                format!(
                    r#"{{"temp_data": "value{}", "old_field": "test{}", "user_name": "User{}"}}"#,
                    i, i, i
                )
            })
            .collect();

        let json_refs: Vec<&str> = json_docs.iter().map(|s| s.as_str()).collect();

        // Sequential processing
        let sequential_result = JSONTools::new()
            .flatten()
            .key_replacement("r'^(temp|old|user)_'", "new_")
            .value_replacement("^test", "updated")
            .parallel_threshold(usize::MAX) // Force sequential
            .execute(json_refs.clone())
            .expect("Sequential processing failed");

        // Parallel processing
        let parallel_result = JSONTools::new()
            .flatten()
            .key_replacement("r'^(temp|old|user)_'", "new_")
            .value_replacement("^test", "updated")
            .parallel_threshold(1) // Force parallel
            .execute(json_refs)
            .expect("Parallel processing failed");

        // Compare results
        let (seq_results, par_results) = match (sequential_result, parallel_result) {
            (JsonOutput::Multiple(seq), JsonOutput::Multiple(par)) => (seq, par),
            _ => panic!("Expected Multiple output"),
        };

        assert_eq!(seq_results.len(), par_results.len());

        for (i, (seq, par)) in seq_results.iter().zip(par_results.iter()).enumerate() {
            assert_eq!(seq, par, "Result {} should be identical", i);
        }
    }

    /// Test thread-local cache isolation
    #[test]
    fn test_thread_local_cache_isolation() {
        // This test verifies that thread-local regex caches don't interfere with each other
        let json_docs: Vec<String> = (0..200)
            .map(|i| {
                format!(
                    r#"{{"field_{}_name": "value{}", "data_{}_id": {}}}"#,
                    i % 10,
                    i,
                    i % 5,
                    i
                )
            })
            .collect();

        let json_refs: Vec<&str> = json_docs.iter().map(|s| s.as_str()).collect();

        // Process with multiple regex patterns
        let result = JSONTools::new()
            .flatten()
            .key_replacement("r'field_[0-9]+_'", "f_")
            .key_replacement("r'data_[0-9]+_'", "d_")
            .value_replacement("r'value([0-9]+)'", "val_$1")
            .parallel_threshold(10)
            .execute(json_refs)
            .expect("Processing failed");

        // Verify all results are correct
        if let JsonOutput::Multiple(results) = result {
            assert_eq!(results.len(), 200);

            for result_str in results.iter() {
                let value: serde_json::Value = serde_json::from_str(result_str).unwrap();
                let obj = value.as_object().unwrap();

                // Check that replacements were applied
                assert!(
                    obj.keys()
                        .any(|k| k.starts_with("f_") || k.starts_with("d_")),
                    "Keys should have replacements applied"
                );
            }
        }
    }

    /// Test adaptive threshold behavior with regex
    #[test]
    fn test_adaptive_threshold_behavior() {
        // Small batch (< threshold) - should use sequential
        let small_batch: Vec<String> = (0..5).map(|i| format!(r#"{{"user_id": {}}}"#, i)).collect();
        let small_refs: Vec<&str> = small_batch.iter().map(|s| s.as_str()).collect();

        let small_result = JSONTools::new()
            .flatten()
            .key_replacement("user_", "")
            .parallel_threshold(10)
            .execute(small_refs)
            .expect("Small batch failed");

        // Large batch (> threshold) - should use parallel
        let large_batch: Vec<String> = (0..50)
            .map(|i| format!(r#"{{"user_id": {}}}"#, i))
            .collect();
        let large_refs: Vec<&str> = large_batch.iter().map(|s| s.as_str()).collect();

        let large_result = JSONTools::new()
            .flatten()
            .key_replacement("user_", "")
            .parallel_threshold(10)
            .execute(large_refs)
            .expect("Large batch failed");

        // Both should succeed
        assert!(matches!(small_result, JsonOutput::Multiple(_)));
        assert!(matches!(large_result, JsonOutput::Multiple(_)));
    }

    /// Test environment variable for parallel threshold
    #[test]
    fn test_environment_variable_threshold() {
        std::env::set_var("JSON_TOOLS_PARALLEL_THRESHOLD", "5");

        let json_docs: Vec<String> = (0..10).map(|i| format!(r#"{{"id": {}}}"#, i)).collect();
        let json_refs: Vec<&str> = json_docs.iter().map(|s| s.as_str()).collect();

        // Should use parallel processing because batch size (10) > threshold (5)
        let result = JSONTools::new()
            .flatten()
            .execute(json_refs)
            .expect("Processing failed");

        assert!(matches!(result, JsonOutput::Multiple(_)));

        std::env::remove_var("JSON_TOOLS_PARALLEL_THRESHOLD");
    }

    // ===== ENHANCED TYPE CONVERSION TESTS =====

    #[test]
    fn test_type_conversion_extended_booleans() {
        let json = r#"{
            "yes_variants": {"a": "yes", "b": "YES", "c": "Yes"},
            "no_variants": {"a": "no", "b": "NO", "c": "No"},
            "y_n": {"a": "y", "b": "Y", "c": "n", "d": "N"},
            "on_off": {"a": "on", "b": "ON", "c": "off", "d": "OFF"},
            "numeric": {"a": "1", "b": "0"}
        }"#;

        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        // Yes variants should be true
        assert_eq!(parsed["yes_variants.a"], true);
        assert_eq!(parsed["yes_variants.b"], true);
        assert_eq!(parsed["yes_variants.c"], true);

        // No variants should be false
        assert_eq!(parsed["no_variants.a"], false);
        assert_eq!(parsed["no_variants.b"], false);
        assert_eq!(parsed["no_variants.c"], false);

        // Y/N variants
        assert_eq!(parsed["y_n.a"], true);
        assert_eq!(parsed["y_n.b"], true);
        assert_eq!(parsed["y_n.c"], false);
        assert_eq!(parsed["y_n.d"], false);

        // On/Off variants
        assert_eq!(parsed["on_off.a"], true);
        assert_eq!(parsed["on_off.b"], true);
        assert_eq!(parsed["on_off.c"], false);
        assert_eq!(parsed["on_off.d"], false);

        // Numeric values (1 and 0 are now treated as numbers, not booleans)
        assert_eq!(parsed["numeric.a"], 1);
        assert_eq!(parsed["numeric.b"], 0);
    }

    #[test]
    fn test_type_conversion_percentages() {
        let json = r#"{
            "percent1": "50%",
            "percent2": "100%",
            "percent3": "0.5%",
            "percent4": "25.75%",
            "negative": "-10%"
        }"#;

        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        // Percentages should be converted to numbers (not decimals)
        assert_eq!(parsed["percent1"], 50.0);
        assert_eq!(parsed["percent2"], 100.0);
        assert_eq!(parsed["percent3"], 0.5);
        assert_eq!(parsed["percent4"], 25.75);
        assert_eq!(parsed["negative"], -10.0);
    }

    #[test]
    fn test_type_conversion_null_strings() {
        let json = r#"{
            "null_variants": {"a": "null", "b": "NULL", "c": "Null"},
            "nil_variants": {"a": "nil", "b": "NIL", "c": "Nil"},
            "none_variants": {"a": "none", "b": "NONE", "c": "None"},
            "na_variants": {"a": "N/A", "b": "n/a", "c": "NA", "d": "na"}
        }"#;

        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        // All null variants should be converted to JSON null
        assert_eq!(parsed["null_variants.a"], Value::Null);
        assert_eq!(parsed["null_variants.b"], Value::Null);
        assert_eq!(parsed["null_variants.c"], Value::Null);

        assert_eq!(parsed["nil_variants.a"], Value::Null);
        assert_eq!(parsed["nil_variants.b"], Value::Null);
        assert_eq!(parsed["nil_variants.c"], Value::Null);

        assert_eq!(parsed["none_variants.a"], Value::Null);
        assert_eq!(parsed["none_variants.b"], Value::Null);
        assert_eq!(parsed["none_variants.c"], Value::Null);

        assert_eq!(parsed["na_variants.a"], Value::Null);
        assert_eq!(parsed["na_variants.b"], Value::Null);
        assert_eq!(parsed["na_variants.c"], Value::Null);
        assert_eq!(parsed["na_variants.d"], Value::Null);
    }

    #[test]
    fn test_type_conversion_mixed_values() {
        let json = r#"{
            "number": "123",
            "percent": "50%",
            "bool_yes": "yes",
            "bool_no": "no",
            "null_str": "null",
            "regular_string": "hello",
            "empty": "",
            "actual_null": null,
            "currency": "$1,234.56"
        }"#;

        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        // Verify each conversion
        assert_eq!(parsed["number"], 123);
        assert_eq!(parsed["percent"], 50.0);
        assert_eq!(parsed["bool_yes"], true);
        assert_eq!(parsed["bool_no"], false);
        assert_eq!(parsed["null_str"], Value::Null);
        assert_eq!(parsed["regular_string"], "hello");
        assert_eq!(parsed["empty"], ""); // Empty strings stay as strings
        assert_eq!(parsed["actual_null"], Value::Null);
        assert_eq!(parsed["currency"], 1234.56);
    }

    #[test]
    fn test_type_conversion_priority() {
        // Test that conversions happen in the right order
        // Priority: null strings > booleans > numbers
        let json = r#"{
            "null_variant": "N/A",
            "bool_variant": "yes",
            "number_variant": "123",
            "one_digit": "1",
            "zero_digit": "0"
        }"#;

        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        // Verify conversion priority
        assert_eq!(parsed["null_variant"], Value::Null); // Null string takes priority
        assert_eq!(parsed["bool_variant"], true); // Boolean conversion
        assert_eq!(parsed["number_variant"], 123); // Number conversion

        // "1" and "0" are now treated as numbers, not booleans
        assert_eq!(parsed["one_digit"], 1);
        assert_eq!(parsed["zero_digit"], 0);
    }

    #[test]
    fn test_type_conversion_no_false_positives() {
        // Strings that look similar but shouldn't convert
        let json = r#"{
            "not_null": "nullify",
            "not_yes": "yesterday",
            "not_no": "normal",
            "not_percent": "percentage",
            "not_number": "1 apple",
            "word_on": "onboard",
            "word_off": "offhand"
        }"#;

        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        // All should remain as strings
        assert_eq!(parsed["not_null"], "nullify");
        assert_eq!(parsed["not_yes"], "yesterday");
        assert_eq!(parsed["not_no"], "normal");
        assert_eq!(parsed["not_percent"], "percentage");
        assert_eq!(parsed["not_number"], "1 apple");
        assert_eq!(parsed["word_on"], "onboard");
        assert_eq!(parsed["word_off"], "offhand");
    }

    #[test]
    fn test_type_conversion_with_unflatten() {
        // Test that type conversion also works with unflatten
        let flattened = r#"{
            "user.id": "123",
            "user.active": "true",
            "user.score": "95.5%",
            "user.status": "null"
        }"#;

        let result = JSONTools::new()
            .unflatten()
            .auto_convert_types(true)
            .execute(flattened)
            .unwrap();
        let unflattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&unflattened).unwrap();

        assert_eq!(parsed["user"]["id"], 123);
        assert_eq!(parsed["user"]["active"], true);
        assert_eq!(parsed["user"]["score"], 95.5);
        assert_eq!(parsed["user"]["status"], Value::Null);
    }

    #[test]
    fn test_enhanced_number_formats() {
        // Test various currency formats, negative numbers, and separators
        let json = r#"{
            "usd": "$1,234.56",
            "eur": "EUR 999.99",
            "gbp": "£50.00",
            "brl": "R$123.45",
            "aud": "A$75.50",
            "neg_standard": "-123.45",
            "neg_accounting": "(456.78)",
            "neg_trailing": "789.12-",
            "neg_bracket": "[321.09]",
            "underscore": "1_000_000",
            "space_sep": "2 500 000",
            "plus": "+42.5"
        }"#;

        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();

        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        // Currency conversions
        assert_eq!(parsed["usd"], 1234.56);
        assert_eq!(parsed["eur"], 999.99);
        assert_eq!(parsed["gbp"], 50.0);
        assert_eq!(parsed["brl"], 123.45);
        assert_eq!(parsed["aud"], 75.5);

        // Negative formats
        assert_eq!(parsed["neg_standard"], -123.45);
        assert_eq!(parsed["neg_accounting"], -456.78);
        assert_eq!(parsed["neg_trailing"], -789.12);
        assert_eq!(parsed["neg_bracket"], -321.09);

        // Alternative separators
        assert_eq!(parsed["underscore"], 1000000);
        assert_eq!(parsed["space_sep"], 2500000);

        // Plus sign
        assert_eq!(parsed["plus"], 42.5);
    }

    #[test]
    fn test_auto_convert_types_and_remove_nulls_interaction() {
        // Test how auto_convert_types and remove_nulls work together
        // Expected behavior:
        // 1. Type conversion runs first (converts string nulls to JSON null)
        // 2. Null removal runs second (removes all null keys)

        let json = r#"{
            "actual_null": null,
            "string_null": "null",
            "string_na": "N/A",
            "string_nil": "nil",
            "string_none": "none",
            "regular_string": "hello",
            "number": "42",
            "boolean": "true"
        }"#;

        // Scenario 1: Only auto_convert_types - converts string nulls to JSON null, keeps all nulls
        let result1 = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();

        let flattened1 = extract_single(result1);
        let parsed1: Value = serde_json::from_str(&flattened1).unwrap();
        assert_eq!(parsed1["actual_null"], Value::Null);
        assert_eq!(parsed1["string_null"], Value::Null); // Converted from "null"
        assert_eq!(parsed1["string_na"], Value::Null); // Converted from "N/A"
        assert_eq!(parsed1["string_nil"], Value::Null); // Converted from "nil"
        assert_eq!(parsed1["string_none"], Value::Null); // Converted from "none"
        assert_eq!(parsed1["regular_string"], "hello");
        assert_eq!(parsed1["number"], 42);
        assert_eq!(parsed1["boolean"], true);

        // Scenario 2: Only remove_nulls - removes existing nulls but doesn't convert string nulls
        let result2 = JSONTools::new()
            .flatten()
            .remove_nulls(true)
            .execute(json)
            .unwrap();

        let flattened2 = extract_single(result2);
        let parsed2: Value = serde_json::from_str(&flattened2).unwrap();
        assert!(parsed2.get("actual_null").is_none()); // Removed
        assert_eq!(parsed2["string_null"], "null"); // Kept as string (not converted)
        assert_eq!(parsed2["string_na"], "N/A"); // Kept as string (not converted)
        assert_eq!(parsed2["string_nil"], "nil"); // Kept as string (not converted)
        assert_eq!(parsed2["string_none"], "none"); // Kept as string (not converted)
        assert_eq!(parsed2["regular_string"], "hello");
        assert_eq!(parsed2["number"], "42"); // Not converted
        assert_eq!(parsed2["boolean"], "true"); // Not converted

        // Scenario 3: Both together - converts string nulls THEN removes all nulls
        let result3 = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .remove_nulls(true)
            .execute(json)
            .unwrap();

        let flattened3 = extract_single(result3);
        let parsed3: Value = serde_json::from_str(&flattened3).unwrap();
        assert!(parsed3.get("actual_null").is_none()); // Removed
        assert!(parsed3.get("string_null").is_none()); // Converted to null, then removed
        assert!(parsed3.get("string_na").is_none()); // Converted to null, then removed
        assert!(parsed3.get("string_nil").is_none()); // Converted to null, then removed
        assert!(parsed3.get("string_none").is_none()); // Converted to null, then removed
        assert_eq!(parsed3["regular_string"], "hello"); // Kept
        assert_eq!(parsed3["number"], 42); // Converted and kept
        assert_eq!(parsed3["boolean"], true); // Converted and kept

        // Verify that only non-null values remain when both are enabled
        assert_eq!(parsed3.as_object().unwrap().len(), 3); // Only 3 keys remain
    }

    #[test]
    fn test_suffixed_numbers() {
        // Test K/M/B/T suffixes for large numbers
        let json = r#"{
            "thousand": "5K",
            "thousand_lower": "2.5k",
            "million": "3M",
            "million_decimal": "1.5m",
            "billion": "2B",
            "trillion": "1T"
        }"#;

        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();

        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        assert_eq!(parsed["thousand"], 5000.0);
        assert_eq!(parsed["thousand_lower"], 2500.0);
        assert_eq!(parsed["million"], 3000000.0);
        assert_eq!(parsed["million_decimal"], 1500000.0);
        assert_eq!(parsed["billion"], 2000000000.0);
        assert_eq!(parsed["trillion"], 1000000000000.0);
    }

    #[test]
    fn test_fractions() {
        // Test fraction parsing
        let json = r#"{
            "half": "1/2",
            "quarter": "1/4",
            "three_quarters": "3/4",
            "mixed_positive": "2 1/2",
            "mixed_negative": "-1 1/2",
            "negative_fraction": "-3/4"
        }"#;

        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();

        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        assert_eq!(parsed["half"], 0.5);
        assert_eq!(parsed["quarter"], 0.25);
        assert_eq!(parsed["three_quarters"], 0.75);
        assert_eq!(parsed["mixed_positive"], 2.5);
        assert_eq!(parsed["mixed_negative"], -1.5);
        assert_eq!(parsed["negative_fraction"], -0.75);
    }

    #[test]
    fn test_radix_numbers() {
        // Test hex, binary, octal parsing
        let json = r#"{
            "hex_lower": "0xff",
            "hex_upper": "0xFF",
            "hex_large": "0x1A2B",
            "binary": "0b1010",
            "binary_upper": "0B1111",
            "octal": "0o777",
            "octal_upper": "0O755",
            "negative_hex": "-0x10"
        }"#;

        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();

        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        assert_eq!(parsed["hex_lower"], 255.0);
        assert_eq!(parsed["hex_upper"], 255.0);
        assert_eq!(parsed["hex_large"], 6699.0); // 0x1A2B = 6699
        assert_eq!(parsed["binary"], 10.0); // 0b1010 = 10
        assert_eq!(parsed["binary_upper"], 15.0); // 0B1111 = 15
        assert_eq!(parsed["octal"], 511.0); // 0o777 = 511
        assert_eq!(parsed["octal_upper"], 493.0); // 0O755 = 493
        assert_eq!(parsed["negative_hex"], -16.0); // -0x10 = -16
    }

    #[test]
    fn test_basis_points() {
        // Test basis points parsing
        let json = r#"{
            "bp_suffix": "25bp",
            "bps_suffix": "50bps",
            "bp_space": "100 bp",
            "bps_space": "75 bps"
        }"#;

        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();

        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        // Basis points: 1bp = 0.0001 (1/100th of a percent)
        assert_eq!(parsed["bp_suffix"], 0.0025); // 25bp = 0.0025
        assert_eq!(parsed["bps_suffix"], 0.005); // 50bps = 0.005
        assert_eq!(parsed["bp_space"], 0.01); // 100bp = 0.01
        assert_eq!(parsed["bps_space"], 0.0075); // 75bps = 0.0075
    }

    #[test]
    fn test_permille() {
        // Test permille (‰) parsing
        let json = r#"{
            "permille": "5‰",
            "per_ten_thousand": "25‱"
        }"#;

        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();

        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        // Permille: 1‰ = 0.001 (per thousand)
        assert_eq!(parsed["permille"], 0.005); // 5‰ = 0.005
                                               // Per ten-thousand: 1‱ = 0.0001
        assert_eq!(parsed["per_ten_thousand"], 0.0025); // 25‱ = 0.0025
    }

    #[test]
    fn test_indian_numbering() {
        // Test Indian numbering system (lakhs and crores)
        let json = r#"{
            "one_lakh": "1,00,000",
            "ten_lakh": "10,00,000",
            "one_crore": "1,00,00,000",
            "mixed": "12,34,567"
        }"#;

        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();

        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        assert_eq!(parsed["one_lakh"], 100000.0); // 1,00,000 = 100,000
        assert_eq!(parsed["ten_lakh"], 1000000.0); // 10,00,000 = 1,000,000
        assert_eq!(parsed["one_crore"], 10000000.0); // 1,00,00,000 = 10,000,000
        assert_eq!(parsed["mixed"], 1234567.0); // 12,34,567 = 1,234,567
    }

    #[test]
    fn test_iso8601_date_detection() {
        // Test ISO-8601 date detection - dates should stay as strings (no JSON date type)
        // but get normalized to UTC
        let json = r#"{
            "date_only": "2024-01-15",
            "datetime_utc": "2024-01-15T10:30:00Z",
            "datetime_no_tz": "2024-01-15T10:30:00",
            "datetime_with_offset": "2024-01-15T10:30:00+05:00",
            "datetime_negative_offset": "2024-01-15T10:30:00-08:00",
            "not_a_date": "2024-13-45",
            "regular_number": "12345"
        }"#;

        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();

        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        // Date-only stays as-is
        assert_eq!(parsed["date_only"], "2024-01-15");

        // UTC datetime stays as-is (already normalized)
        assert_eq!(parsed["datetime_utc"], "2024-01-15T10:30:00Z");

        // Naive datetime assumed UTC, normalized with Z suffix
        assert_eq!(parsed["datetime_no_tz"], "2024-01-15T10:30:00Z");

        // +05:00 offset → UTC is 5 hours earlier
        assert_eq!(parsed["datetime_with_offset"], "2024-01-15T05:30:00Z");

        // -08:00 offset → UTC is 8 hours later
        assert_eq!(parsed["datetime_negative_offset"], "2024-01-15T18:30:00Z");

        // Invalid date stays as string (not converted)
        assert_eq!(parsed["not_a_date"], "2024-13-45");

        // Regular numbers still convert to numbers
        assert_eq!(parsed["regular_number"], 12345);
    }

    #[test]
    fn test_iso8601_datetime_with_fractional_seconds() {
        // Test datetime with fractional seconds
        let json = r#"{
            "with_millis": "2024-06-15T14:30:45.123Z",
            "with_micros": "2024-06-15T14:30:45.123456Z",
            "no_tz_with_millis": "2024-06-15T14:30:45.500"
        }"#;

        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();

        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        // Normalized to UTC without fractional seconds
        assert_eq!(parsed["with_millis"], "2024-06-15T14:30:45Z");
        assert_eq!(parsed["with_micros"], "2024-06-15T14:30:45Z");
        assert_eq!(parsed["no_tz_with_millis"], "2024-06-15T14:30:45Z");
    }

    #[test]
    fn test_iso8601_space_separator() {
        // Test datetime with space separator instead of T
        let json = r#"{
            "space_datetime": "2024-01-15 10:30:00",
            "space_with_tz": "2024-01-15 10:30:00+02:00"
        }"#;

        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();

        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        // Space separator normalized to T with Z suffix
        assert_eq!(parsed["space_datetime"], "2024-01-15T10:30:00Z");

        // Space with timezone normalized to UTC
        assert_eq!(parsed["space_with_tz"], "2024-01-15T08:30:00Z");
    }

    #[test]
    fn test_date_not_confused_with_numbers() {
        // Ensure dates are not accidentally converted to numbers
        let json = r#"{
            "date": "2024-01-15",
            "looks_like_math": "2024-01-15",
            "timestamp": "2024-12-25T00:00:00Z"
        }"#;

        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();

        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        // Dates should remain as strings, not converted to numbers
        assert!(parsed["date"].is_string());
        assert!(parsed["looks_like_math"].is_string());
        assert!(parsed["timestamp"].is_string());

        // Verify they are valid date strings
        assert_eq!(parsed["date"], "2024-01-15");
        assert_eq!(parsed["timestamp"], "2024-12-25T00:00:00Z");
    }

    #[test]
    fn test_compact_date_format() {
        // Test compact ISO-8601 date: YYYYMMDD
        let json = r#"{
            "compact_date": "20240115",
            "compact_datetime": "20240115T103000",
            "compact_datetime_z": "20240115T103000Z",
            "compact_with_offset": "20240115T103000+0530"
        }"#;

        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();

        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        // Compact date normalized to YYYY-MM-DD
        assert_eq!(parsed["compact_date"], "2024-01-15");

        // Compact datetime normalized to ISO format with Z
        assert_eq!(parsed["compact_datetime"], "2024-01-15T10:30:00Z");
        assert_eq!(parsed["compact_datetime_z"], "2024-01-15T10:30:00Z");

        // Compact with offset normalized to UTC
        // 10:30:00+05:30 = 05:00:00Z
        assert_eq!(parsed["compact_with_offset"], "2024-01-15T05:00:00Z");
    }

    #[test]
    fn test_ordinal_date_format() {
        // Test ordinal date: YYYY-DDD (day of year)
        let json = r#"{
            "jan_15": "2024-015",
            "dec_31": "2024-366",
            "leap_year": "2024-060"
        }"#;

        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();

        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        // Ordinal dates normalized to YYYY-MM-DD
        assert_eq!(parsed["jan_15"], "2024-01-15");
        assert_eq!(parsed["dec_31"], "2024-12-31"); // 2024 is leap year
        assert_eq!(parsed["leap_year"], "2024-02-29"); // Day 60 in leap year
    }

    #[test]
    fn test_week_date_format() {
        // Test ISO week date: YYYY-Www-D
        let json = r#"{
            "week_with_day": "2024-W03-1",
            "week_friday": "2024-W03-5"
        }"#;

        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();

        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        // Week dates normalized to YYYY-MM-DD
        // Week 3 of 2024: Jan 15-21
        assert_eq!(parsed["week_with_day"], "2024-01-15"); // Monday
        assert_eq!(parsed["week_friday"], "2024-01-19"); // Friday
    }

    #[test]
    fn test_alternate_separators() {
        // Test dates with slash and dot separators
        let json = r#"{
            "slash_date": "2024/01/15",
            "dot_date": "2024.01.15",
            "slash_datetime": "2024/01/15T10:30:00Z",
            "dot_datetime": "2024.01.15T10:30:00+02:00"
        }"#;

        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();

        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        // Normalized to standard format
        assert_eq!(parsed["slash_date"], "2024-01-15");
        assert_eq!(parsed["dot_date"], "2024-01-15");
        assert_eq!(parsed["slash_datetime"], "2024-01-15T10:30:00Z");
        // +02:00 offset -> 2 hours earlier in UTC
        assert_eq!(parsed["dot_datetime"], "2024-01-15T08:30:00Z");
    }

    #[test]
    fn test_timezone_offset_variants() {
        // Test various timezone offset formats
        let json = r#"{
            "colon_offset": "2024-01-15T10:30:00+05:30",
            "no_colon_offset": "2024-01-15T10:30:00+0530",
            "hour_only_offset": "2024-01-15T10:30:00+05",
            "negative_offset": "2024-01-15T10:30:00-0800",
            "zulu": "2024-01-15T10:30:00Z"
        }"#;

        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();

        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        // All should normalize to UTC
        assert_eq!(parsed["colon_offset"], "2024-01-15T05:00:00Z"); // +05:30
        assert_eq!(parsed["no_colon_offset"], "2024-01-15T05:00:00Z"); // +0530
        assert_eq!(parsed["hour_only_offset"], "2024-01-15T05:30:00Z"); // +05:00
        assert_eq!(parsed["negative_offset"], "2024-01-15T18:30:00Z"); // -08:00
        assert_eq!(parsed["zulu"], "2024-01-15T10:30:00Z");
    }

    #[test]
    fn test_datetime_without_seconds() {
        // Test datetime formats without seconds
        let json = r#"{
            "no_seconds": "2024-01-15T10:30",
            "no_seconds_z": "2024-01-15T10:30Z"
        }"#;

        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();

        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        // Normalized with :00 seconds added
        assert_eq!(parsed["no_seconds"], "2024-01-15T10:30:00Z");
        assert_eq!(parsed["no_seconds_z"], "2024-01-15T10:30:00Z");
    }
}

// ==========================================
// JsonOutput try_into tests
// ==========================================

#[cfg(test)]
mod json_output_tests {
    use crate::JsonOutput;

    #[test]
    fn test_try_into_single_ok() {
        let output = JsonOutput::Single(r#"{"a":1}"#.to_string());
        assert_eq!(output.try_into_single().unwrap(), r#"{"a":1}"#);
    }

    #[test]
    fn test_try_into_single_err() {
        let output = JsonOutput::Multiple(vec![r#"{"a":1}"#.to_string()]);
        assert!(output.try_into_single().is_err());
    }

    #[test]
    fn test_try_into_multiple_ok() {
        let output = JsonOutput::Multiple(vec![r#"{"a":1}"#.to_string()]);
        assert_eq!(output.try_into_multiple().unwrap(), vec![r#"{"a":1}"#]);
    }

    #[test]
    fn test_try_into_multiple_err() {
        let output = JsonOutput::Single(r#"{"a":1}"#.to_string());
        assert!(output.try_into_multiple().is_err());
    }
}

// ==========================================
// max_array_index DoS protection tests
// ==========================================

#[cfg(test)]
mod max_array_index_tests {
    use crate::tests::extract_single;
    use crate::JSONTools;
    use serde_json::Value;

    #[test]
    fn test_max_array_index_rejects_huge_index() {
        let json = r#"{"items.999999999": "value"}"#;
        let result = JSONTools::new().unflatten().execute(json);
        assert!(result.is_err());
        let err = result.unwrap_err();
        assert!(err.to_string().contains("exceeds maximum"));
    }

    #[test]
    fn test_max_array_index_accepts_small_index() {
        let json = r#"{"items.5": "value"}"#;
        let result = JSONTools::new().unflatten().execute(json);
        assert!(result.is_ok());
    }

    #[test]
    fn test_max_array_index_custom_limit() {
        let json = r#"{"items.11": "value"}"#;
        // Custom limit of 10 should reject index 11
        let result = JSONTools::new()
            .unflatten()
            .max_array_index(10)
            .execute(json);
        assert!(result.is_err());

        // But index 9 should be fine
        let json_ok = r#"{"items.9": "value"}"#;
        let result_ok = JSONTools::new()
            .unflatten()
            .max_array_index(10)
            .execute(json_ok);
        assert!(result_ok.is_ok());
    }

    #[test]
    fn test_array_index_overflow_converts_to_object() {
        // A digit-only key that overflows `usize` (25 nines) is *not* caught by
        // the `max_array_index` bounds check -- that check only runs after
        // `.parse::<usize>()` already succeeded. Such a key still passes the
        // digits-only `is_valid_array_index` check used by the whole-document
        // path-type pre-analysis, so the parent path is classified as an array
        // up front; `.parse::<usize>()` then fails during tree-building, which
        // must fall back to converting the in-progress array into an object
        // (see `set_nested_value_recursive`'s "Non-numeric key in array
        // context" branch) rather than erroring or silently dropping data.
        let json = r#"{"items.0": "a", "items.1": "b", "items.99999999999999999999999": "c"}"#;
        let result = JSONTools::new().unflatten().execute(json).unwrap();
        let processed = extract_single(result);
        let parsed: Value = serde_json::from_str(&processed).unwrap();

        assert!(parsed["items"].is_object(), "items should become an object");
        assert_eq!(parsed["items"]["0"], "a");
        assert_eq!(parsed["items"]["1"], "b");
        assert_eq!(parsed["items"]["99999999999999999999999"], "c");
    }
}

// ==========================================
// Validation, edge case, and normal mode tests
// ==========================================

#[cfg(test)]
mod validation_and_edge_case_tests {
    use crate::tests::{extract_multiple, extract_single};
    use crate::JSONTools;
    use serde_json::Value;

    #[test]
    fn test_empty_separator_returns_error() {
        let result = JSONTools::new()
            .flatten()
            .separator("")
            .execute(r#"{"a": 1}"#);
        assert!(result.is_err());
        let err = result.unwrap_err();
        assert!(err.to_string().contains("Separator cannot be empty"));
    }

    #[test]
    fn test_num_threads_zero_returns_error() {
        let result = JSONTools::new()
            .flatten()
            .num_threads(Some(0))
            .execute(r#"{"a": 1}"#);
        assert!(result.is_err());
        let err = result.unwrap_err();
        assert!(err.to_string().contains("num_threads must be at least 1"));
    }

    #[test]
    fn test_execute_without_mode_returns_error() {
        let result = JSONTools::new().execute(r#"{"a": 1}"#);
        assert!(result.is_err());
        let err = result.unwrap_err();
        assert!(err.to_string().contains("Operation mode not set"));
    }

    #[test]
    fn test_max_array_index_enforcement() {
        // Very large index should be rejected with default limit
        let json = r#"{"items.999999999": "value"}"#;
        let result = JSONTools::new().unflatten().execute(json);
        assert!(result.is_err());
    }

    #[test]
    fn test_unicode_keys_flatten() {
        let json = r#"{"用户": {"名前": "太郎", "émoji": "🎉"}}"#;
        let result = JSONTools::new().flatten().execute(json).unwrap();
        let flattened = extract_single(result);
        let parsed: Value = serde_json::from_str(&flattened).unwrap();

        assert_eq!(parsed["用户.名前"], "太郎");
        assert_eq!(parsed["用户.émoji"], "🎉");
    }

    #[test]
    fn test_unicode_keys_roundtrip() {
        let json = r#"{"café": {"naïve": "résumé"}, "日本語": {"キー": "値"}}"#;
        let flattened = JSONTools::new().flatten().execute(json).unwrap();
        let flat_str = extract_single(flattened);
        let unflattened = JSONTools::new()
            .unflatten()
            .execute(flat_str.as_str())
            .unwrap();
        let result = extract_single(unflattened);
        let parsed: Value = serde_json::from_str(&result).unwrap();

        assert_eq!(parsed["café"]["naïve"], "résumé");
        assert_eq!(parsed["日本語"]["キー"], "値");
    }

    #[test]
    fn test_unicode_value_with_escape_sequence() {
        // Regression test: unescape_json_string previously reinterpreted each byte of a
        // multi-byte UTF-8 sequence as a separate Latin-1 codepoint whenever the string
        // also contained a JSON escape sequence (e.g. \n), corrupting non-ASCII text.
        let json =
            r#"{"note": "café\nrésumé", "emoji": "hi 👍\tthere", "mixed": "日本語\"quoted\""}"#;
        let flattened = JSONTools::new().flatten().execute(json).unwrap();
        let flat_str = extract_single(flattened);
        let parsed: Value = serde_json::from_str(&flat_str).unwrap();

        assert_eq!(parsed["note"], "café\nrésumé");
        assert_eq!(parsed["emoji"], "hi 👍\tthere");
        assert_eq!(parsed["mixed"], "日本語\"quoted\"");
    }

    #[test]
    fn test_key_with_escape_sequence_produces_valid_json() {
        // Regression test: DirectWalker (flatten's fast path, no key transforms
        // configured) used to unescape a key's escape sequences to build the path but
        // never re-escape before writing that path directly as the output key. Any key
        // containing an escaped quote/backslash/control char therefore produced
        // syntactically invalid JSON output (an unescaped `"` terminating the key
        // string early). Covers both a top-level key and a key at nesting depth 2.
        let json = r#"{"café \"nested\" city": "v1", "user": {"say \"hi\"": "v2"}}"#;
        let flattened = JSONTools::new().flatten().execute(json).unwrap();
        let flat_str = extract_single(flattened);
        let parsed: Value =
            serde_json::from_str(&flat_str).expect("flatten output must be valid JSON");

        assert_eq!(parsed["café \"nested\" city"], "v1");
        assert_eq!(parsed["user.say \"hi\""], "v2");
    }

    #[test]
    fn test_key_and_value_escaping_preserves_multibyte_utf8() {
        // Regression test: escape_json_string/write_json_escaped_key's slow path (taken
        // whenever a string has at least one char needing escaping) previously
        // reinterpreted each byte of a multi-byte UTF-8 sequence as its own Latin-1
        // codepoint via `push(b as char)` -- the same bug class already fixed in
        // unescape_json_string (see test_unicode_value_with_escape_sequence), but
        // present here in the opposite (re-escaping) direction. Exercises: the
        // CollectingWalker slow path (lowercase_keys forces it) for key escaping, and
        // value_replacement (which routes through escape_json_string) for value
        // escaping. Mixes Latin accents, CJK, Cyrillic, and emoji with embedded quotes.
        let json = r#"{"名前_\"test\"_émoji_😀_ключ": "OLD café_\"val\"_中文_🎉"}"#;
        let flattened = JSONTools::new()
            .flatten()
            .lowercase_keys(true)
            .value_replacement("OLD ", "NEW ")
            .execute(json)
            .unwrap();
        let flat_str = extract_single(flattened);
        let parsed: Value =
            serde_json::from_str(&flat_str).expect("flatten output must be valid JSON");

        let expected_key = "名前_\"test\"_émoji_😀_ключ".to_lowercase();
        assert_eq!(parsed[&expected_key], "NEW café_\"val\"_中文_🎉");
    }

    #[test]
    fn test_unflatten_key_escaping_preserves_multibyte_utf8() {
        // Same bug as test_key_and_value_escaping_preserves_multibyte_utf8, exercised
        // through unflatten.rs's key serialization (which reuses flatten.rs's
        // write_json_escaped_key).
        let flat_json = r#"{"café \"nested\"_日本語_🎉 city": "v"}"#;
        let unflattened = JSONTools::new().unflatten().execute(flat_json).unwrap();
        let result = extract_single(unflattened);
        let parsed: Value =
            serde_json::from_str(&result).expect("unflatten output must be valid JSON");

        assert_eq!(parsed["café \"nested\"_日本語_🎉 city"], "v");
    }

    /// Builds a deeply-nested (5 levels) JSON object with `width` keys at each level,
    /// so flattened leaf paths are long enough (>24 bytes) to exceed CompactString's
    /// inline cap and exercise the sequential slow path's bump-arena key storage
    /// (`BumpKeyBuilder`) rather than a shallow/coincidentally-inline case.
    fn deeply_nested_json(width: usize) -> String {
        let mut obj = serde_json::Map::new();
        for i in 0..width {
            obj.insert(
                format!("Leaf_Field_{i}"),
                serde_json::Value::String(format!("value_{i}")),
            );
        }
        let mut value = serde_json::Value::Object(obj);
        for level in ["levelFour", "levelThree", "levelTwo", "levelOne"] {
            let mut wrapper = serde_json::Map::new();
            wrapper.insert(level.to_string(), value);
            value = serde_json::Value::Object(wrapper);
        }
        serde_json::to_string(&value).unwrap()
    }

    #[test]
    fn test_bump_arena_deep_nesting_lowercase() {
        let json = deeply_nested_json(10);
        let flattened = JSONTools::new()
            .flatten()
            .lowercase_keys(true)
            .execute(json.as_str())
            .unwrap();
        let flat_str = extract_single(flattened);
        let parsed: Value = serde_json::from_str(&flat_str).expect("must be valid JSON");

        for i in 0..10 {
            let key = format!("levelone.leveltwo.levelthree.levelfour.leaf_field_{i}");
            assert_eq!(parsed[&key], format!("value_{i}"), "missing key: {key}");
        }
        assert_eq!(parsed.as_object().unwrap().len(), 10);
    }

    #[test]
    fn test_bump_arena_deep_nesting_key_replacement() {
        let json = deeply_nested_json(8);
        let flattened = JSONTools::new()
            .flatten()
            .key_replacement("r'Leaf_Field_'", "field_")
            .key_replacement("r'level(One|Two|Three|Four)'", "L")
            .execute(json.as_str())
            .unwrap();
        let flat_str = extract_single(flattened);
        let parsed: Value = serde_json::from_str(&flat_str).expect("must be valid JSON");

        for i in 0..8 {
            let key = format!("L.L.L.L.field_{i}");
            assert_eq!(parsed[&key], format!("value_{i}"), "missing key: {key}");
        }
    }

    #[test]
    fn test_bump_arena_deep_nesting_collision_handling() {
        // Two distinct source paths that collapse to the same key after lowercasing,
        // deep enough to hit the bump-arena path -- exercises resolve_and_write's
        // collision map (FxHashMap<&str, ...>) with bump-backed keys specifically.
        let json = r#"{
            "levelOne": {"levelTwo": {"levelThree": {"levelFour": {"DupField": "first"}}}},
            "levelOneAlt": {"levelTwo": {"levelThree": {"levelFour": {"dupfield": "second"}}}}
        }"#;
        let flattened = JSONTools::new()
            .flatten()
            .lowercase_keys(true)
            // Lowercase runs before replacement (pre-existing, documented order), so
            // the pattern must match already-lowercased text.
            .key_replacement("r'^levelonealt'", "levelone")
            .handle_key_collision(true)
            .execute(json)
            .unwrap();
        let flat_str = extract_single(flattened);
        let parsed: Value = serde_json::from_str(&flat_str).expect("must be valid JSON");

        let key = "levelone.leveltwo.levelthree.levelfour.dupfield";
        let arr = parsed[key]
            .as_array()
            .expect("collision should merge to array");
        assert_eq!(arr.len(), 2);
        assert!(arr.contains(&Value::String("first".to_string())));
        assert!(arr.contains(&Value::String("second".to_string())));
    }

    #[test]
    fn test_bump_arena_deep_nesting_all_transforms_combined() {
        // lowercase + key_replacement + collision handling all at once, plus a
        // multi-byte UTF-8 + escaped-quote key mixed in for good measure.
        let json = r#"{
            "LevelOne": {"LevelTwo": {"LevelThree": {"LevelFour": {
                "USER_Name": "Alice",
                "café_\"special\"_日本語": "café_val"
            }}}}
        }"#;
        let flattened = JSONTools::new()
            .flatten()
            .lowercase_keys(true)
            // No `^` anchor: key_replacement matches against the full dotted path, and
            // "user_" is the start of the *last* segment here, not the whole path.
            .key_replacement("r'(user|admin)_'", "")
            .handle_key_collision(true)
            .execute(json)
            .unwrap();
        let flat_str = extract_single(flattened);
        let parsed: Value =
            serde_json::from_str(&flat_str).expect("flatten output must be valid JSON");

        assert_eq!(
            parsed["levelone.leveltwo.levelthree.levelfour.name"],
            "Alice"
        );
        assert_eq!(
            parsed["levelone.leveltwo.levelthree.levelfour.café_\"special\"_日本語"],
            "café_val"
        );
    }

    #[test]
    fn test_nested_parallel_path_still_correct_with_key_transforms() {
        // Forces flatten_collecting_parallel (CompactKeyBuilder path, not the bump
        // arena) via a low threshold, combined with key transforms -- confirms the
        // generic CollectedEntry<K>/KeyBuilder refactor didn't change behavior on the
        // parallel path, which intentionally still uses CompactString.
        let mut obj = serde_json::Map::new();
        for i in 0..50 {
            obj.insert(format!("Field_{i}"), serde_json::json!({"Nested_Value": i}));
        }
        let json = serde_json::to_string(&serde_json::Value::Object(obj)).unwrap();

        let flattened = JSONTools::new()
            .flatten()
            .lowercase_keys(true)
            .nested_parallel_threshold(10) // 50 top-level children > 10: forces parallel path
            .execute(json.as_str())
            .unwrap();
        let flat_str = extract_single(flattened);
        let parsed: Value = serde_json::from_str(&flat_str).expect("must be valid JSON");

        for i in 0..50 {
            let key = format!("field_{i}.nested_value");
            assert_eq!(parsed[&key], i, "missing key: {key}");
        }
        assert_eq!(parsed.as_object().unwrap().len(), 50);
    }

    #[test]
    fn test_escaped_value_falls_through_replacement_to_auto_convert() {
        // Regression test combining two fixes: (1) a perf fix where value_replacement +
        // auto_convert_types together used to unescape the same string twice when the
        // replacement pattern didn't match, and (2) the has_escape scanner bug covered in
        // detail by test_scanner_detects_non_quote_escapes below -- "123\t" only exercises
        // auto_convert_types at all once the scanner correctly flags it as escaped. Covers
        // both the DirectWalker path (no key transforms) and the CollectingWalker path
        // (lowercase_keys forces it).
        let json = r#"{"Count": "123\t", "Label": "hello\nworld"}"#;

        // DirectWalker path: value_replacement (non-matching) + auto_convert_types.
        let direct = JSONTools::new()
            .flatten()
            .value_replacement("NOMATCH", "x")
            .auto_convert_types(true)
            .execute(json)
            .unwrap();
        let direct_parsed: Value = serde_json::from_str(&extract_single(direct)).unwrap();
        assert_eq!(direct_parsed["Count"], 123);
        assert_eq!(direct_parsed["Label"], "hello\nworld");

        // CollectingWalker path: same, plus lowercase_keys to force the collecting path.
        let collecting = JSONTools::new()
            .flatten()
            .value_replacement("NOMATCH", "x")
            .auto_convert_types(true)
            .lowercase_keys(true)
            .execute(json)
            .unwrap();
        let collecting_parsed: Value = serde_json::from_str(&extract_single(collecting)).unwrap();
        assert_eq!(collecting_parsed["count"], 123);
        assert_eq!(collecting_parsed["label"], "hello\nworld");
    }

    #[test]
    fn test_scanner_detects_non_quote_escapes() {
        // Regression test: the tape scanner's has_escape bit was only set by detecting
        // escaped quotes (\") or backslash-runs immediately preceding a quote character --
        // it used memchr to jump straight to the next `"`, so any escape sequence that
        // wasn't adjacent to a quote (\n, \t, \r, \b, \f, \/, \uXXXX, or a lone \\ in the
        // middle of a string) was invisible to it. Any feature gated on string_has_escapes()
        // (auto_convert_types, value_replacement, key_replacement, lowercase_keys, collision
        // handling) silently skipped unescaping such strings. auto_convert_types is the
        // clearest way to observe this: a numeric string is only recognized as a number
        // after correct unescaping + trimming.
        let cases = [
            (r#"{"n": "42\t"}"#, "n", 42),
            (r#"{"n": "42\n"}"#, "n", 42),
            (r#"{"n": "42\r"}"#, "n", 42),
            (r#"{"n": "\t42"}"#, "n", 42),
            (r#"{"n": "\n\r\t42\n\r\t"}"#, "n", 42),
        ];

        for (json, key, expected) in cases {
            let result = JSONTools::new()
                .flatten()
                .auto_convert_types(true)
                .execute(json)
                .unwrap();
            let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
            assert_eq!(
                parsed[key], expected,
                "failed to auto-convert {json:?} (has_escape must be true for whitespace-only escapes)"
            );
        }

        // \uXXXX (unicode escape, not adjacent to a quote) must also be detected and
        // correctly unescaped when a transform needs the real text: "Café" is the
        // JSON-escaped form of "Café" and contains a literal backslash nowhere near a
        // quote character. A literal (non-regex) value_replacement only matches against
        // the real, unescaped text, so this only succeeds if has_escape was set correctly.
        let json = "{\"Name\": \"Caf\\u00e9\"}";
        let result = JSONTools::new()
            .flatten()
            .value_replacement("Café", "Kaffee")
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert_eq!(parsed["Name"], "Kaffee");
    }

    #[test]
    fn test_normal_mode_lowercase_keys() {
        let json = r#"{"UserName": "John", "UserAge": 30, "nested": {"InnerKey": true}}"#;
        let result = JSONTools::new()
            .normal()
            .lowercase_keys(true)
            .execute(json)
            .unwrap();
        let output = extract_single(result);
        let parsed: Value = serde_json::from_str(&output).unwrap();

        assert_eq!(parsed["username"], "John");
        assert_eq!(parsed["userage"], 30);
        assert_eq!(parsed["nested"]["innerkey"], true);
    }

    #[test]
    fn test_normal_mode_auto_convert_types() {
        let json = r#"{"count": "42", "active": "true", "rate": "3.14"}"#;
        let result = JSONTools::new()
            .normal()
            .auto_convert_types(true)
            .execute(json)
            .unwrap();
        let output = extract_single(result);
        let parsed: Value = serde_json::from_str(&output).unwrap();

        assert_eq!(parsed["count"], 42);
        assert_eq!(parsed["active"], true);
        assert!(parsed["rate"].is_f64());
    }

    #[test]
    fn test_normal_mode_filtering() {
        let json = r#"{"a": "", "b": null, "c": {}, "d": [], "e": "keep"}"#;
        let result = JSONTools::new()
            .normal()
            .remove_empty_strings(true)
            .remove_nulls(true)
            .remove_empty_objects(true)
            .remove_empty_arrays(true)
            .execute(json)
            .unwrap();
        let output = extract_single(result);
        let parsed: Value = serde_json::from_str(&output).unwrap();

        assert!(parsed.get("a").is_none());
        assert!(parsed.get("b").is_none());
        assert!(parsed.get("c").is_none());
        assert!(parsed.get("d").is_none());
        assert_eq!(parsed["e"], "keep");
    }

    #[test]
    fn test_batch_processing_error_includes_index() {
        let inputs: Vec<&str> = vec![r#"{"a": 1}"#, "not valid json", r#"{"b": 2}"#];
        let result = JSONTools::new().flatten().execute(inputs.as_slice());
        assert!(result.is_err());
        let err = result.unwrap_err();
        // The error should mention the index of the failed item
        assert!(err.to_string().contains("1") || err.to_string().contains("index"));
    }

    #[test]
    fn test_json_output_try_into_single() {
        let result = JSONTools::new().flatten().execute(r#"{"a": 1}"#).unwrap();
        assert!(result.try_into_single().is_ok());
    }

    #[test]
    fn test_json_output_try_into_multiple_from_single_errors() {
        let result = JSONTools::new().flatten().execute(r#"{"a": 1}"#).unwrap();
        assert!(result.try_into_multiple().is_err());
    }

    #[test]
    fn test_json_output_into_vec_single() {
        let result = JSONTools::new().flatten().execute(r#"{"a": 1}"#).unwrap();
        let vec = result.into_vec();
        assert_eq!(vec.len(), 1);
    }

    // ===== FINE-GRAINED TYPE CONVERSION TESTS =====

    #[test]
    fn test_convert_dates_independent() {
        // Only dates enabled: date strings normalize, null/boolean/number strings
        // stay untouched.
        let json = r#"{"d": "2024-01-15T10:30:00+05:00", "n": "null", "b": "true", "num": "123"}"#;
        let result = JSONTools::new()
            .flatten()
            .convert_dates(true)
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();

        assert_eq!(parsed["d"], "2024-01-15T05:30:00Z");
        assert_eq!(parsed["n"], "null"); // still a string, not JSON null
        assert_eq!(parsed["b"], "true"); // still a string, not JSON true
        assert_eq!(parsed["num"], "123"); // still a string, not JSON number
    }

    #[test]
    fn test_convert_nulls_independent() {
        let json = r#"{"n": "null", "b": "true", "num": "123"}"#;
        let result = JSONTools::new()
            .flatten()
            .convert_nulls(true)
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();

        assert!(parsed["n"].is_null());
        assert_eq!(parsed["b"], "true");
        assert_eq!(parsed["num"], "123");
    }

    #[test]
    fn test_convert_booleans_independent() {
        let json = r#"{"n": "null", "b": "true", "num": "123"}"#;
        let result = JSONTools::new()
            .flatten()
            .convert_booleans(true)
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();

        assert_eq!(parsed["n"], "null");
        assert_eq!(parsed["b"], true);
        assert_eq!(parsed["num"], "123");
    }

    #[test]
    fn test_convert_numbers_independent() {
        let json = r#"{"n": "null", "b": "true", "num": "123", "price": "$45.67"}"#;
        let result = JSONTools::new()
            .flatten()
            .convert_numbers(true)
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();

        assert_eq!(parsed["n"], "null");
        assert_eq!(parsed["b"], "true");
        assert_eq!(parsed["num"], 123);
        assert_eq!(parsed["price"], 45.67);
    }

    #[test]
    fn test_auto_convert_types_then_per_category_disable() {
        // Call order: auto_convert_types(true) then convert_dates(false) -- dates
        // should stay off, other three categories on.
        let json = r#"{"d": "2024-01-15T10:30:00Z", "b": "true", "num": "123"}"#;
        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .convert_dates(false)
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();

        assert_eq!(parsed["d"], "2024-01-15T10:30:00Z"); // unchanged string, not re-parsed as a number
        assert_eq!(parsed["b"], true);
        assert_eq!(parsed["num"], 123);
    }

    #[test]
    fn test_per_category_disable_then_auto_convert_types_reenables() {
        // Call order reversed: convert_dates(false) then auto_convert_types(true) --
        // last-call-wins means auto_convert_types(true) re-enables dates too.
        let json = r#"{"d": "2024-01-15T10:30:00+05:00"}"#;
        let result = JSONTools::new()
            .flatten()
            .convert_dates(false)
            .auto_convert_types(true)
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();

        assert_eq!(parsed["d"], "2024-01-15T05:30:00Z");
    }

    #[test]
    fn test_auto_convert_types_preserves_prior_customization() {
        // A per-category customization set before auto_convert_types(true) must
        // survive -- auto_convert_types only ever flips the `enabled` bit, it must
        // not reset sub-settings back to their own defaults.
        let json = r#"{"d": "2024-01-15T10:30:00"}"#; // naive datetime
        let result = JSONTools::new()
            .flatten()
            .convert_dates_config(
                crate::DateConversionConfig::new()
                    .enabled(false)
                    .assume_utc_for_naive(false),
            )
            .auto_convert_types(true)
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();

        // enabled flips true (auto_convert_types wins), but assume_utc_for_naive(false)
        // must still be respected -- naive datetime left unchanged.
        assert_eq!(parsed["d"], "2024-01-15T10:30:00");
    }

    #[test]
    fn test_convert_nulls_extra_tokens_additive() {
        let json = r#"{"a": "missing", "b": "N/A", "c": "not_a_token"}"#;
        let result = JSONTools::new()
            .flatten()
            .convert_nulls_config(
                crate::NullConversionConfig::new()
                    .enabled(true)
                    .add_extra_token("missing"),
            )
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();

        assert!(parsed["a"].is_null()); // extra token
        assert!(parsed["b"].is_null()); // built-in list still active
        assert_eq!(parsed["c"], "not_a_token");
    }

    #[test]
    fn test_convert_booleans_extra_tokens_additive() {
        let json = r#"{"a": "si", "b": "nope", "c": "true", "d": "not_a_token"}"#;
        let result = JSONTools::new()
            .flatten()
            .convert_booleans_config(
                crate::BooleanConversionConfig::new()
                    .enabled(true)
                    .add_extra_true_token("si")
                    .add_extra_false_token("nope"),
            )
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();

        assert_eq!(parsed["a"], true); // extra true token
        assert_eq!(parsed["b"], false); // extra false token
        assert_eq!(parsed["c"], true); // built-in list still active
        assert_eq!(parsed["d"], "not_a_token");
    }

    #[test]
    fn test_convert_dates_normalize_to_utc_false() {
        // Offset-bearing datetime left byte-for-byte unchanged, but still protected
        // from falling through to number parsing.
        let json = r#"{"d": "2024-01-15T10:30:00+05:00"}"#;
        let result = JSONTools::new()
            .flatten()
            .convert_dates_config(
                crate::DateConversionConfig::new()
                    .enabled(true)
                    .normalize_to_utc(false),
            )
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();

        assert_eq!(parsed["d"], "2024-01-15T10:30:00+05:00");
    }

    #[test]
    fn test_convert_dates_assume_utc_for_naive_false() {
        // Naive (timezone-less) datetime left unchanged -- no `Z` appended.
        let json = r#"{"d": "2024-01-15T10:30:00"}"#;
        let result = JSONTools::new()
            .flatten()
            .convert_dates_config(
                crate::DateConversionConfig::new()
                    .enabled(true)
                    .assume_utc_for_naive(false),
            )
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();

        assert_eq!(parsed["d"], "2024-01-15T10:30:00");
    }

    #[test]
    fn test_convert_numbers_currency_disabled() {
        let json = r#"{"price": "$45.67", "count": "1,234.56"}"#;
        let result = JSONTools::new()
            .flatten()
            .convert_numbers_config(
                crate::NumberConversionConfig::new()
                    .enabled(true)
                    .currency(false),
            )
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();

        assert_eq!(parsed["price"], "$45.67"); // currency stripping disabled
        assert_eq!(parsed["count"], 1234.56); // thousands-separator cleanup still core behavior
    }

    #[test]
    fn test_convert_numbers_percent_disabled() {
        let json = r#"{"pct": "50%", "count": "123"}"#;
        let result = JSONTools::new()
            .flatten()
            .convert_numbers_config(
                crate::NumberConversionConfig::new()
                    .enabled(true)
                    .percent(false),
            )
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();

        assert_eq!(parsed["pct"], "50%");
        assert_eq!(parsed["count"], 123);
    }

    #[test]
    fn test_convert_numbers_basis_points_disabled() {
        let json = r#"{"bp": "25bps", "count": "123"}"#;
        let result = JSONTools::new()
            .flatten()
            .convert_numbers_config(
                crate::NumberConversionConfig::new()
                    .enabled(true)
                    .basis_points(false),
            )
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();

        assert_eq!(parsed["bp"], "25bps");
        assert_eq!(parsed["count"], 123);
    }

    #[test]
    fn test_convert_numbers_suffixes_disabled() {
        let json = r#"{"mag": "2.5M", "count": "123"}"#;
        let result = JSONTools::new()
            .flatten()
            .convert_numbers_config(
                crate::NumberConversionConfig::new()
                    .enabled(true)
                    .suffixes(false),
            )
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();

        assert_eq!(parsed["mag"], "2.5M");
        assert_eq!(parsed["count"], 123);
    }

    #[test]
    fn test_convert_numbers_fractions_disabled() {
        let json = r#"{"frac": "1/2", "count": "123"}"#;
        let result = JSONTools::new()
            .flatten()
            .convert_numbers_config(
                crate::NumberConversionConfig::new()
                    .enabled(true)
                    .fractions(false),
            )
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();

        assert_eq!(parsed["frac"], "1/2");
        assert_eq!(parsed["count"], 123);
    }

    #[test]
    fn test_convert_numbers_radix_disabled() {
        let json = r#"{"hex": "0x1A", "count": "123"}"#;
        let result = JSONTools::new()
            .flatten()
            .convert_numbers_config(
                crate::NumberConversionConfig::new()
                    .enabled(true)
                    .radix(false),
            )
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();

        assert_eq!(parsed["hex"], "0x1A");
        assert_eq!(parsed["count"], 123);
    }

    #[test]
    fn test_normal_mode_fine_grained_type_conversion() {
        // Fine-grained categories must work identically in normal mode (nesting
        // preserved), matching auto_convert_types' existing "works for all
        // operations" guarantee.
        let json = r#"{"user": {"active": "true", "id": "42"}}"#;
        let result = JSONTools::new()
            .normal()
            .convert_booleans(true)
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();

        assert_eq!(parsed["user"]["active"], true);
        assert_eq!(parsed["user"]["id"], "42"); // numbers category not enabled
    }

    #[test]
    fn test_unflatten_fine_grained_type_conversion() {
        let json = r#"{"user.active": "true", "user.id": "42"}"#;
        let result = JSONTools::new()
            .unflatten()
            .convert_booleans(true)
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();

        assert_eq!(parsed["user"]["active"], true);
        assert_eq!(parsed["user"]["id"], "42");
    }

    #[test]
    fn test_type_conversion_mode_classify() {
        use crate::config::{
            BooleanConversionConfig, DateConversionConfig, NullConversionConfig,
            NumberConversionConfig, TypeConversionConfig, TypeConversionMode,
        };

        assert_eq!(
            TypeConversionConfig::new().classify(),
            TypeConversionMode::Disabled
        );

        let all_default = TypeConversionConfig::new()
            .dates(DateConversionConfig::new().enabled(true))
            .nulls(NullConversionConfig::new().enabled(true))
            .booleans(BooleanConversionConfig::new().enabled(true))
            .numbers(NumberConversionConfig::new().enabled(true));
        assert_eq!(all_default.classify(), TypeConversionMode::AllDefault);

        // Single-category enable (not all four) is Custom.
        let partial =
            TypeConversionConfig::new().numbers(NumberConversionConfig::new().enabled(true));
        assert_eq!(partial.classify(), TypeConversionMode::Custom);

        // All four enabled but one knob deviates from default is Custom.
        let custom = TypeConversionConfig::new()
            .dates(
                DateConversionConfig::new()
                    .enabled(true)
                    .normalize_to_utc(false),
            )
            .nulls(NullConversionConfig::new().enabled(true))
            .booleans(BooleanConversionConfig::new().enabled(true))
            .numbers(NumberConversionConfig::new().enabled(true));
        assert_eq!(custom.classify(), TypeConversionMode::Custom);
    }

    #[test]
    fn test_auto_convert_types_is_all_default_mode() {
        // Regression guard for the hot-path claim: JSONTools::auto_convert_types(true)
        // (with no per-category customization) must classify as AllDefault, so it
        // routes through the untouched, unmodified original fast-path function.
        let tools = JSONTools::new().flatten().auto_convert_types(true);
        let config = crate::config::ProcessingConfig::from_json_tools(&tools);
        assert_eq!(
            config.type_conversion_mode,
            crate::config::TypeConversionMode::AllDefault
        );
    }

    // ===== FINE-GRAINED TYPE CONVERSION EDGE CASES =====

    #[test]
    fn test_convert_numbers_all_subformats_disabled_core_still_works() {
        // Every "opinionated" sub-format off; plain integers/decimals, scientific
        // notation, and thousands-separator cleanup are always-on core behavior and
        // must still work.
        let json = r#"{
            "int": "123",
            "dec": "45.67",
            "neg": "-10",
            "sci": "1.23e-4",
            "us_thousands": "1,234.56",
            "eu_thousands": "1.234,56",
            "currency": "$99.99",
            "pct": "50%",
            "bp": "25bps",
            "suffixed": "2.5M",
            "fraction": "1/2",
            "hex": "0x1A"
        }"#;
        let result = JSONTools::new()
            .flatten()
            .convert_numbers_config(
                crate::NumberConversionConfig::new()
                    .enabled(true)
                    .currency(false)
                    .percent(false)
                    .basis_points(false)
                    .suffixes(false)
                    .fractions(false)
                    .radix(false),
            )
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();

        // Core: always converts.
        assert_eq!(parsed["int"], 123);
        assert_eq!(parsed["dec"], 45.67);
        assert_eq!(parsed["neg"], -10);
        assert_eq!(parsed["sci"], 0.000123);
        assert_eq!(parsed["us_thousands"], 1234.56);
        assert_eq!(parsed["eu_thousands"], 1234.56);
        // Opinionated sub-formats: all disabled, all stay as the original string.
        assert_eq!(parsed["currency"], "$99.99");
        assert_eq!(parsed["pct"], "50%");
        assert_eq!(parsed["bp"], "25bps");
        assert_eq!(parsed["suffixed"], "2.5M");
        assert_eq!(parsed["fraction"], "1/2");
        assert_eq!(parsed["hex"], "0x1A");
    }

    #[test]
    fn test_convert_numbers_radix_disabled_negative_hex_stays_string() {
        // A negative radix-looking string must not be picked up by any other
        // sub-format when radix is disabled -- it should fall through untouched,
        // not get mangled by the always-on core parser.
        let json = r#"{"a": "-0x1A", "b": "-123"}"#;
        let result = JSONTools::new()
            .flatten()
            .convert_numbers_config(
                crate::NumberConversionConfig::new()
                    .enabled(true)
                    .radix(false),
            )
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();

        assert_eq!(parsed["a"], "-0x1A"); // radix disabled, not a valid plain number either
        assert_eq!(parsed["b"], -123); // core plain-number parsing unaffected
    }

    #[test]
    fn test_convert_booleans_token_in_both_lists_true_wins() {
        // A token added to both extra_true_tokens and extra_false_tokens is an
        // ambiguous user configuration; lock in the actual (deterministic)
        // precedence rather than leaving it unspecified: true is checked first.
        let json = r#"{"a": "maybe"}"#;
        let result = JSONTools::new()
            .flatten()
            .convert_booleans_config(
                crate::BooleanConversionConfig::new()
                    .enabled(true)
                    .add_extra_true_token("maybe")
                    .add_extra_false_token("maybe"),
            )
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert_eq!(parsed["a"], true);
    }

    #[test]
    fn test_convert_nulls_extra_token_duplicating_builtin_is_harmless() {
        // Adding an extra token that's already in the built-in list must not
        // panic or double-count; behavior is identical to not adding it.
        let json = r#"{"a": "null", "b": "not_null"}"#;
        let result = JSONTools::new()
            .flatten()
            .convert_nulls_config(
                crate::NullConversionConfig::new()
                    .enabled(true)
                    .add_extra_token("null"),
            )
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert!(parsed["a"].is_null());
        assert_eq!(parsed["b"], "not_null");
    }

    #[test]
    fn test_extra_tokens_match_after_trimming_not_raw_bytes() {
        // Extra tokens are matched against the *trimmed* value, consistent with
        // every other category and the built-in token lists (e.g. `auto_convert_types`
        // already converts `" 123 "` to `123`) -- not a byte-for-byte match against
        // the untrimmed raw string. Discovered while porting this exact case to the
        // Python test suite (an initial "trailing space should NOT match" assumption
        // was wrong).
        let json = r#"{"a": "si ", "b": " si", "c": "siX"}"#;
        let result = JSONTools::new()
            .flatten()
            .convert_booleans_config(
                crate::BooleanConversionConfig::new()
                    .enabled(true)
                    .add_extra_true_token("si"),
            )
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert_eq!(parsed["a"], true); // trailing whitespace trimmed before comparison
        assert_eq!(parsed["b"], true); // leading whitespace trimmed before comparison
        assert_eq!(parsed["c"], "siX"); // not a match at all -- extra text, not whitespace
    }

    #[test]
    fn test_disabled_category_customization_has_no_effect() {
        // A category left disabled must produce zero observable effect even when
        // it carries leftover/inert customization -- confirms `enabled` really
        // gates everything, and that a still-Custom-mode classification (since the
        // config deviates from the "all four AllDefault" shape) doesn't leak any
        // partial behavior for the disabled category.
        let json = r#"{"price": "$45.67", "count": "123"}"#;
        let result = JSONTools::new()
            .flatten()
            .convert_numbers_config(
                crate::NumberConversionConfig::new()
                    .enabled(false)
                    .currency(false), // inert: category itself is off
            )
            .convert_booleans(true) // ensures TypeConversionMode::Custom is reached
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        // Numbers category entirely off: neither value converts, regardless of
        // the inert `currency(false)` setting.
        assert_eq!(parsed["price"], "$45.67");
        assert_eq!(parsed["count"], "123");
    }

    #[test]
    fn test_date_priority_wins_over_null_extra_token() {
        // Dates are checked before nulls in priority order. A string that's both a
        // valid recognized date AND (contrived) also configured as an extra null
        // token must still be date-normalized, not nulled out -- priority order
        // must hold even when a later category's customization could also match.
        let json = r#"{"d": "2024-01-15T10:30:00+05:00"}"#;
        let result = JSONTools::new()
            .flatten()
            .convert_dates(true)
            .convert_nulls_config(
                crate::NullConversionConfig::new()
                    .enabled(true)
                    .add_extra_token("2024-01-15T10:30:00+05:00"),
            )
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert_eq!(parsed["d"], "2024-01-15T05:30:00Z"); // date normalization won, not null
    }

    #[test]
    fn test_null_extra_token_wins_when_dates_disabled() {
        // Same contrived string as above, but with dates disabled this time --
        // the null category's extra-token fallback should now be free to match it.
        let json = r#"{"d": "2024-01-15T10:30:00+05:00"}"#;
        let result = JSONTools::new()
            .flatten()
            .convert_nulls_config(
                crate::NullConversionConfig::new()
                    .enabled(true)
                    .add_extra_token("2024-01-15T10:30:00+05:00"),
            )
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert!(parsed["d"].is_null());
    }

    #[test]
    fn test_fine_grained_type_conversion_in_batch() {
        // The Custom-mode dispatch must work correctly across a whole batch
        // (including the parallel dispatch path for batches at/above
        // parallel_threshold), not just a single document.
        let batch: Vec<String> = (0..150)
            .map(|i| format!(r#"{{"id": "{i}", "active": "yes", "extra": "missing"}}"#))
            .collect();
        let tools = JSONTools::new()
            .flatten()
            .convert_numbers(true)
            .convert_booleans(true)
            .convert_nulls_config(
                crate::NullConversionConfig::new()
                    .enabled(true)
                    .add_extra_token("missing"),
            );
        let results = extract_multiple(tools.execute(batch.as_slice()).unwrap());
        assert_eq!(results.len(), 150);
        for (i, r) in results.iter().enumerate() {
            let parsed: Value = serde_json::from_str(r).unwrap();
            assert_eq!(parsed["id"], i as i64);
            assert_eq!(parsed["active"], true);
            assert!(parsed["extra"].is_null());
        }
    }

    #[test]
    fn test_classify_disabled_even_with_inert_leftover_customization() {
        use crate::config::{
            BooleanConversionConfig, NumberConversionConfig, TypeConversionConfig,
            TypeConversionMode,
        };

        // `has_any_enabled()` is checked first: a config where every category is
        // disabled correctly classifies as Disabled (the cheapest dispatch path)
        // even when a disabled category carries leftover/inert customization --
        // classify() doesn't need to inspect sub-settings at all once nothing is
        // enabled.
        let all_disabled_with_junk = TypeConversionConfig::new()
            .numbers(NumberConversionConfig::new().enabled(false).currency(false))
            .booleans(
                BooleanConversionConfig::new()
                    .enabled(false)
                    .add_extra_true_token("x"),
            );
        assert_eq!(
            all_disabled_with_junk.classify(),
            TypeConversionMode::Disabled
        );

        // Once *something* is enabled, a disabled-but-customized category still
        // makes the overall config deviate from the "all four AllDefault" shape,
        // so classify() correctly falls to Custom (see
        // test_disabled_category_customization_has_no_effect for the behavioral
        // guarantee this dispatch decision must not break -- the disabled
        // category's customization stays functionally inert either way).
        let one_enabled_one_disabled_with_junk = TypeConversionConfig::new()
            .numbers(NumberConversionConfig::new().enabled(false).currency(false))
            .booleans(BooleanConversionConfig::new().enabled(true));
        assert_eq!(
            one_enabled_one_disabled_with_junk.classify(),
            TypeConversionMode::Custom
        );
    }

    #[test]
    fn test_numeric_extra_boolean_token_loses_to_numbers_when_both_enabled() {
        // A numeric-looking extra token ("1") is reachable only via the fallback
        // pass at the end of `try_convert_string_to_json_bytes_configured` (see its
        // doc comment) -- but the digit-dispatch arm tries numbers *before* falling
        // through to that pass, so when numbers is also enabled, plain number
        // parsing claims "1" first and the fallback is never reached. Non-obvious
        // enough to lock in explicitly rather than leave undocumented.
        let json = r#"{"a": "1"}"#;
        let result = JSONTools::new()
            .flatten()
            .convert_numbers(true)
            .convert_booleans_config(
                crate::BooleanConversionConfig::new()
                    .enabled(true)
                    .add_extra_true_token("1"),
            )
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert_eq!(parsed["a"], 1); // number, not boolean
    }

    #[test]
    fn test_numeric_extra_boolean_token_wins_when_numbers_disabled() {
        // Same input as above, but with numbers disabled -- now nothing claims "1"
        // via the digit-dispatch arm, so the fallback pass reaches the extra token.
        let json = r#"{"a": "1"}"#;
        let result = JSONTools::new()
            .flatten()
            .convert_booleans_config(
                crate::BooleanConversionConfig::new()
                    .enabled(true)
                    .add_extra_true_token("1"),
            )
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert_eq!(parsed["a"], true); // boolean, via the extra-token fallback
    }

    #[test]
    fn test_extra_tokens_are_case_sensitive() {
        let json = r#"{"a": "missing", "b": "MISSING"}"#;
        let result = JSONTools::new()
            .flatten()
            .convert_nulls_config(
                crate::NullConversionConfig::new()
                    .enabled(true)
                    .add_extra_token("missing"),
            )
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert!(parsed["a"].is_null());
        assert_eq!(parsed["b"], "MISSING"); // different case, no match
    }

    #[test]
    fn test_malformed_date_stays_as_string_no_crash() {
        // A string that superficially looks date-shaped (passes `could_be_date`'s
        // cheap prefilter) but has out-of-range components must not panic and must
        // be left untouched, exactly like the original (non-fine-grained) behavior.
        let json = r#"{"a": "2024-13-45T99:99:99"}"#;
        let result = JSONTools::new()
            .flatten()
            .convert_dates(true)
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert_eq!(parsed["a"], "2024-13-45T99:99:99");
    }

    #[test]
    fn test_invalid_leap_year_date_stays_as_string() {
        // 2023 is not a leap year -- "2023-02-29" looks date-shaped but
        // NaiveDate::from_ymd_opt correctly rejects it, so it's not recognized as a
        // date at all and must fall through (safely, without corruption) rather
        // than being misinterpreted as a number.
        let json = r#"{"a": "2023-02-29"}"#;
        let result = JSONTools::new()
            .flatten()
            .convert_dates(true)
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert_eq!(parsed["a"], "2023-02-29");
    }

    #[test]
    fn test_valid_leap_year_date_recognized_but_unchanged() {
        // 2024 is a leap year -- "2024-02-29" is a genuinely valid date, recognized
        // and left unchanged because it's already canonical (date-only, no
        // time/offset to normalize).
        let json = r#"{"a": "2024-02-29"}"#;
        let result = JSONTools::new()
            .flatten()
            .convert_dates(true)
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert_eq!(parsed["a"], "2024-02-29");
    }

    #[test]
    fn test_compact_naive_datetime_through_configured_path() {
        // Compact format (YYYYMMDDTHHMMSS, no separators) exercises a different
        // internal sub-parser than the standard YYYY-MM-DD format used elsewhere
        // in this test suite -- confirms `has_explicit_timezone`'s compact-format
        // fallback branch (checking for '-' past the fixed 15-char prefix) doesn't
        // misfire on a naive compact datetime with no dashes at all.
        let json = r#"{"a": "20240115T103000"}"#;

        let default_result = JSONTools::new()
            .flatten()
            .convert_dates(true)
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(default_result)).unwrap();
        assert_eq!(parsed["a"], "2024-01-15T10:30:00Z"); // normalized + reformatted

        let no_naive_utc_result = JSONTools::new()
            .flatten()
            .convert_dates_config(
                crate::DateConversionConfig::new()
                    .enabled(true)
                    .assume_utc_for_naive(false),
            )
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(no_naive_utc_result)).unwrap();
        assert_eq!(parsed["a"], "20240115T103000"); // left byte-for-byte unchanged
    }

    #[test]
    fn test_extra_null_token_respects_remove_nulls_filtering() {
        // A value converted to null via an *extra* token must be filtered exactly
        // like a built-in-recognized null, confirming filtering runs after the
        // configured conversion path, not just the AllDefault one.
        let json = r#"{"a": "missing", "b": "keep"}"#;
        let result = JSONTools::new()
            .flatten()
            .convert_nulls_config(
                crate::NullConversionConfig::new()
                    .enabled(true)
                    .add_extra_token("missing"),
            )
            .remove_nulls(true)
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert!(parsed.get("a").is_none());
        assert_eq!(parsed["b"], "keep");
    }

    #[test]
    fn test_replacement_and_conversion_chain_identically_across_modes() {
        // Previously an architectural inconsistency: `.flatten()`/`.unflatten()`
        // returned as soon as a value_replacement matched, without ever trying type
        // conversion on the replaced value, while `.normal()` already chained
        // replacement into conversion. Fixed so all three modes compose identically
        // -- this is what makes `remove_nulls` reliably catch a null that only
        // emerges after a replacement runs, regardless of mode. Locking in the now-
        // unified behavior so a future refactor of any of the three walkers doesn't
        // silently reintroduce the inconsistency.
        let json = r#"{"a": "ACTIVE"}"#;

        let flatten_result = JSONTools::new()
            .flatten()
            .value_replacement("ACTIVE", "true")
            .convert_booleans(true)
            .execute(json)
            .unwrap();
        assert_eq!(
            serde_json::from_str::<Value>(&extract_single(flatten_result)).unwrap()["a"],
            true // chained: replacement's output was then converted
        );

        let unflatten_json = r#"{"a": "ACTIVE"}"#;
        let unflatten_result = JSONTools::new()
            .unflatten()
            .value_replacement("ACTIVE", "true")
            .convert_booleans(true)
            .execute(unflatten_json)
            .unwrap();
        assert_eq!(
            serde_json::from_str::<Value>(&extract_single(unflatten_result)).unwrap()["a"],
            true
        );

        let normal_result = JSONTools::new()
            .normal()
            .value_replacement("ACTIVE", "true")
            .convert_booleans(true)
            .execute(json)
            .unwrap();
        assert_eq!(
            serde_json::from_str::<Value>(&extract_single(normal_result)).unwrap()["a"],
            true
        );
    }

    #[test]
    fn test_remove_nulls_catches_null_produced_by_replacement_then_conversion_flatten() {
        // Direct regression test for the ordering fix: a value_replacement turns
        // "MISSING" into "N/A" (a recognized null token), which auto_convert_types
        // then converts to JSON null, which remove_nulls must then catch -- all
        // three have to compose in that order for this to work.
        let json = r#"{"user": {"name": "John", "status": "MISSING", "city": "NYC"}}"#;
        let result = JSONTools::new()
            .flatten()
            .value_replacement("MISSING", "N/A")
            .auto_convert_types(true)
            .remove_nulls(true)
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert_eq!(parsed["user.name"], "John");
        assert_eq!(parsed["user.city"], "NYC");
        assert!(!parsed.as_object().unwrap().contains_key("user.status"));
    }

    #[test]
    fn test_remove_nulls_catches_null_produced_by_replacement_then_conversion_unflatten() {
        let flat_json = r#"{"user.name": "John", "user.status": "MISSING", "user.city": "NYC"}"#;
        let result = JSONTools::new()
            .unflatten()
            .value_replacement("MISSING", "N/A")
            .auto_convert_types(true)
            .remove_nulls(true)
            .execute(flat_json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert_eq!(parsed["user"]["name"], "John");
        assert_eq!(parsed["user"]["city"], "NYC");
        assert!(!parsed["user"].as_object().unwrap().contains_key("status"));
    }

    #[test]
    fn test_remove_nulls_catches_null_produced_by_replacement_then_conversion_normal() {
        let json = r#"{"user": {"name": "John", "status": "MISSING", "city": "NYC"}}"#;
        let result = JSONTools::new()
            .normal()
            .value_replacement("MISSING", "N/A")
            .auto_convert_types(true)
            .remove_nulls(true)
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert_eq!(parsed["user"]["name"], "John");
        assert_eq!(parsed["user"]["city"], "NYC");
        assert!(!parsed["user"].as_object().unwrap().contains_key("status"));
    }

    #[test]
    fn test_remove_nulls_ordering_fix_applies_to_batch_input() {
        // Same compound scenario as the single-document tests above, run as a batch,
        // confirming per-document behavior is identical (process_batch just calls
        // the same per-document processor for each item, so this is a fast check --
        // not expected to fail, but locks in that batching doesn't change anything).
        let batch = vec![
            r#"{"user": {"name": "John", "status": "MISSING"}}"#,
            r#"{"user": {"name": "Jane", "status": "ACTIVE"}}"#,
        ];
        let result = JSONTools::new()
            .flatten()
            .value_replacement("MISSING", "N/A")
            .auto_convert_types(true)
            .remove_nulls(true)
            .execute(batch)
            .unwrap();
        let results = extract_multiple(result);
        assert_eq!(results.len(), 2);

        let first: Value = serde_json::from_str(&results[0]).unwrap();
        assert_eq!(first["user.name"], "John");
        assert!(!first.as_object().unwrap().contains_key("user.status"));

        let second: Value = serde_json::from_str(&results[1]).unwrap();
        assert_eq!(second["user.name"], "Jane");
        assert_eq!(second["user.status"], "ACTIVE");
    }

    #[test]
    fn test_flatten_root_primitive_now_type_converts() {
        // Regression test: flatten's root-primitive branch (whole document is a bare
        // scalar, not an object/array) previously only applied value_replacement and
        // skipped type_conversion (and therefore remove_nulls) entirely. Now composes
        // both, matching the nested-value path.
        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(r#""N/A""#)
            .unwrap();
        assert_eq!(extract_single(result), "null");

        // Replacement composed with conversion at the root, too.
        let replaced = JSONTools::new()
            .flatten()
            .value_replacement("MISSING", "N/A")
            .auto_convert_types(true)
            .execute(r#""MISSING""#)
            .unwrap();
        assert_eq!(extract_single(replaced), "null");
    }

    #[test]
    fn test_unflatten_root_primitive_now_type_converts() {
        let result = JSONTools::new()
            .unflatten()
            .auto_convert_types(true)
            .execute(r#""N/A""#)
            .unwrap();
        assert_eq!(extract_single(result), "null");
    }

    #[test]
    fn test_remove_nulls_cannot_remove_the_document_root() {
        // A root-level null (the entire document, not a nested key) can't be
        // "removed" -- there's no parent key to omit it under. Must stay a
        // documented no-op across every mode that can reach this path.
        let flatten_result = JSONTools::new()
            .flatten()
            .remove_nulls(true)
            .execute("null")
            .unwrap();
        assert_eq!(extract_single(flatten_result), "null");

        let normal_result = JSONTools::new()
            .normal()
            .remove_nulls(true)
            .execute("null")
            .unwrap();
        assert_eq!(extract_single(normal_result), "null");

        // Also verify the root-primitive conversion+removal combination stays a
        // no-op: converting "N/A" to null at the root, with remove_nulls(true), must
        // still return the converted null rather than erroring or emitting nothing.
        let converted_root = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .remove_nulls(true)
            .execute(r#""N/A""#)
            .unwrap();
        assert_eq!(extract_single(converted_root), "null");
    }

    #[test]
    fn test_keys_are_never_type_converted() {
        // Only values are ever candidates for type conversion; a key that happens
        // to look like a recognized token must never be touched.
        let json = r#"{"true": "something", "123": "also something"}"#;
        let result = JSONTools::new()
            .flatten()
            .convert_booleans(true)
            .convert_numbers(true)
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert_eq!(parsed["true"], "something");
        assert_eq!(parsed["123"], "also something");
    }

    #[test]
    fn test_number_subformats_individually_enabled() {
        // Complementary to the existing "disable one, rest default true" tests:
        // here only one sub-format is explicitly true and the rest explicitly
        // false, confirming each flag genuinely gates its own format independent
        // of the others (not just "everything but this one" coverage).
        let json = r#"{"currency": "$45.67", "pct": "50%", "frac": "1/2", "core": "123"}"#;
        let result = JSONTools::new()
            .flatten()
            .convert_numbers_config(
                crate::NumberConversionConfig::new()
                    .enabled(true)
                    .currency(true)
                    .percent(false)
                    .basis_points(false)
                    .suffixes(false)
                    .fractions(false)
                    .radix(false),
            )
            .execute(json)
            .unwrap();
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert_eq!(parsed["currency"], 45.67); // the one enabled sub-format
        assert_eq!(parsed["pct"], "50%"); // disabled
        assert_eq!(parsed["frac"], "1/2"); // disabled
        assert_eq!(parsed["core"], 123); // always-on core parsing
    }

    // ============================================================================
    // Regression tests: UTF-8 char-boundary panics in auto_convert_types
    // (github.com/amaye15/JSON-Tools-rs/issues/29, point 1)
    //
    // Both bugs were fixed-byte-offset string slices (`&s[..3]`, `&s[..N]`) that
    // assumed a specific byte offset was a char boundary without checking, when a
    // multi-byte UTF-8 character could land exactly on that offset. Every case
    // here panicked with "byte index N is not a char boundary" before the fix in
    // src/convert.rs (`strip_currency_indicators`'s 3-letter-code check, and
    // `try_parse_compact_datetime`'s +HHMM offset formatter); each is reproduced
    // here with the exact multi-byte character positioned to straddle the
    // vulnerable offset, not just "any accented string", so a future regression
    // that shifts the bug to a different offset still gets caught.
    // ============================================================================

    /// `strip_currency_indicators`'s "first 3 bytes look like a currency code"
    /// check (src/convert.rs, guarded by `is_char_boundary(3)`). `Á` is 2 bytes,
    /// so `"5xÁ1000"` has a character straddling byte offset 3 exactly.
    #[test]
    fn test_auto_convert_no_panic_currency_code_check_multibyte_straddle() {
        let cases = [
            r#"{"amount": "5xÁ1000"}"#,
            r#"{"amount": "1xÁ2345"}"#,
            r#"{"amount": "5€ García"}"#,
            r#"{"amount": "GAÁ 100"}"#,
            r#"{"n": "0xÁ1F"}"#,
            r#"{"n": "0bÁ101"}"#,
            r#"{"n": "0oÁ17"}"#,
        ];
        for json in cases {
            let result = JSONTools::new()
                .flatten()
                .auto_convert_types(true)
                .execute(json)
                .unwrap_or_else(|e| panic!("{json} should not error, got: {e}"));
            // Not a valid currency-coded number -- must be left as a string,
            // unmodified, not silently truncated or corrupted.
            let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
            let (_, value) = parsed.as_object().unwrap().iter().next().unwrap();
            assert!(
                value.is_string(),
                "{json} -> expected string, got {value:?}"
            );
        }
    }

    /// `try_parse_compact_datetime`'s "+HHMM -> +HH:MM" offset formatter
    /// (src/convert.rs, guarded by `is_char_boundary(3)`). `Á` is 2 bytes, so an
    /// offset of `"+1Á2"` has a character straddling byte offset 3 of the
    /// 5-byte offset substring exactly.
    #[test]
    fn test_auto_convert_no_panic_datetime_offset_multibyte_straddle() {
        let json = r#"{"d": "20240115T103000+1Á2"}"#;
        let result = JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(json)
            .unwrap_or_else(|e| panic!("{json} should not error, got: {e}"));
        // Not a valid timezone offset -- must be left as a string, not parsed
        // as a date (and, above all, must not panic).
        let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
        assert_eq!(parsed["d"], "20240115T103000+1Á2");
    }

    /// The exact repro from the filed issue: an accented name must never panic
    /// `auto_convert_types`, and -- unlike the `.encode("ascii", "ignore")`
    /// workaround the issue describes -- must round-trip with zero data loss.
    #[test]
    fn test_auto_convert_no_panic_accented_names_roundtrip_exactly() {
        let cases = [
            ("García", "García"),
            ("Ángel", "Ángel"),
            ("Zoëy", "Zoëy"),
            ("café", "café"),
            ("naïve résumé", "naïve résumé"),
            ("北京", "北京"),
            ("Müller", "Müller"),
            ("José", "José"),
        ];
        for (input, expected) in cases {
            let json = serde_json::json!({"name": input}).to_string();
            let result = JSONTools::new()
                .flatten()
                .auto_convert_types(true)
                .execute(json.as_str())
                .unwrap_or_else(|e| panic!("{input:?} should not error, got: {e}"));
            let parsed: Value = serde_json::from_str(&extract_single(result)).unwrap();
            assert_eq!(parsed["name"], expected, "input {input:?} corrupted");
        }
    }

    /// Broad sweep: a multi-byte character inserted at every byte position (0
    /// through len) of several representative number/date/currency-shaped
    /// strings must never panic, regardless of exactly where it lands. This is
    /// deliberately more exhaustive than the two exact reproductions above --
    /// it's the regression net for "the same class of bug at a different
    /// offset", not just the two specific offsets already found and fixed.
    #[test]
    fn test_auto_convert_no_panic_multibyte_at_every_position() {
        let templates = [
            "USD 1000",
            "5000 CR",
            "1,234.50",
            "20240115T103000Z",
            "20240115T103000+0500",
            "2024-01-15T10:30:00+05:00",
            "1/2",
            "1 1/2",
            "0x1F",
            "50%",
            "25bps",
            "1.5k",
        ];
        for template in templates {
            for byte_pos in 0..=template.len() {
                // Skip positions that would themselves split a (currently
                // all-ASCII) template mid-character -- not applicable here
                // since every template is pure ASCII, so every byte_pos is a
                // valid insertion point.
                let mut mutated = String::with_capacity(template.len() + 2);
                mutated.push_str(&template[..byte_pos]);
                mutated.push('Á'); // 2-byte UTF-8 character
                mutated.push_str(&template[byte_pos..]);
                let json = serde_json::json!({"v": mutated}).to_string();
                let tools = JSONTools::new().flatten().auto_convert_types(true);
                let outcome = std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| {
                    tools.execute(json.as_str())
                }));
                assert!(
                    outcome.is_ok(),
                    "panicked on template {template:?} with 'Á' inserted at byte {byte_pos}"
                );
            }
        }
    }
}
