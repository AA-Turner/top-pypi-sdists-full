use std::collections::HashMap;

use crate::params::parse_threat_detection_risk_levels;

// ---------------------------------------------------------------------------
// parse_threat_detection_risk_levels
// ---------------------------------------------------------------------------

#[test]
fn test_empty_params_returns_empty_maps() {
    let params = HashMap::new();
    let (deny, allow) = parse_threat_detection_risk_levels(&params);
    assert!(
        deny.is_empty(),
        "deny_tags should be empty when param is absent"
    );
    assert!(
        allow.is_empty(),
        "allow_tags should be empty when param is absent"
    );
}

#[test]
fn test_empty_string_param_returns_empty_maps() {
    let mut params = HashMap::new();
    params.insert("threat_detection_risk_levels".to_string(), String::new());
    let (deny, allow) = parse_threat_detection_risk_levels(&params);
    assert!(deny.is_empty());
    assert!(allow.is_empty());
}

#[test]
fn test_valid_deny_patterns_populated() {
    let json = r#"{
        "critical": {
            "tags": {
                "deny": [{"tag": "rm -rf"}, {"tag": "shutdown"}],
                "allow": []
            }
        }
    }"#;
    let mut params = HashMap::new();
    params.insert("threat_detection_risk_levels".to_string(), json.to_string());
    let (deny, allow) = parse_threat_detection_risk_levels(&params);

    assert_eq!(deny.get("critical").map(|v| v.len()), Some(2));
    assert!(deny["critical"].contains(&"rm -rf".to_string()));
    assert!(deny["critical"].contains(&"shutdown".to_string()));
    assert!(
        allow.is_empty(),
        "allow_tags should be empty when allow array is empty"
    );
}

#[test]
fn test_valid_allow_patterns_populated() {
    let json = r#"{
        "high": {
            "tags": {
                "deny": [],
                "allow": [{"tag": "git status"}, {"tag": "ls"}]
            }
        }
    }"#;
    let mut params = HashMap::new();
    params.insert("threat_detection_risk_levels".to_string(), json.to_string());
    let (deny, allow) = parse_threat_detection_risk_levels(&params);

    assert!(
        deny.is_empty(),
        "deny_tags should be empty when deny array is empty"
    );
    assert_eq!(allow.get("high").map(|v| v.len()), Some(2));
    assert!(allow["high"].contains(&"git status".to_string()));
    assert!(allow["high"].contains(&"ls".to_string()));
}

#[test]
fn test_both_deny_and_allow_across_multiple_levels() {
    let json = r#"{
        "critical": {
            "tags": {
                "deny": [{"tag": "drop table"}],
                "allow": []
            }
        },
        "medium": {
            "tags": {
                "deny": [],
                "allow": [{"tag": "select \\*"}]
            }
        },
        "high": {
            "tags": {
                "deny": [{"tag": "truncate"}],
                "allow": [{"tag": "show tables"}]
            }
        }
    }"#;
    let mut params = HashMap::new();
    params.insert("threat_detection_risk_levels".to_string(), json.to_string());
    let (deny, allow) = parse_threat_detection_risk_levels(&params);

    // critical: only deny
    assert_eq!(deny.get("critical").map(|v| v.len()), Some(1));
    assert!(deny["critical"].contains(&"drop table".to_string()));
    assert!(!allow.contains_key("critical"));

    // medium: only allow
    assert!(!deny.contains_key("medium"));
    assert_eq!(allow.get("medium").map(|v| v.len()), Some(1));

    // high: both
    assert_eq!(deny.get("high").map(|v| v.len()), Some(1));
    assert!(deny["high"].contains(&"truncate".to_string()));
    assert_eq!(allow.get("high").map(|v| v.len()), Some(1));
    assert!(allow["high"].contains(&"show tables".to_string()));
}

#[test]
fn test_invalid_json_returns_empty_maps() {
    let mut params = HashMap::new();
    params.insert(
        "threat_detection_risk_levels".to_string(),
        "not valid json {{{".to_string(),
    );
    let (deny, allow) = parse_threat_detection_risk_levels(&params);
    assert!(
        deny.is_empty(),
        "deny_tags should be empty on JSON parse error"
    );
    assert!(
        allow.is_empty(),
        "allow_tags should be empty on JSON parse error"
    );
}

#[test]
fn test_level_with_empty_tag_arrays_not_included_in_maps() {
    let json = r#"{
        "low": {
            "tags": {
                "deny": [],
                "allow": []
            }
        }
    }"#;
    let mut params = HashMap::new();
    params.insert("threat_detection_risk_levels".to_string(), json.to_string());
    let (deny, allow) = parse_threat_detection_risk_levels(&params);

    // Level with empty arrays should not appear as a key in either map
    assert!(
        !deny.contains_key("low"),
        "level with empty deny should not be in deny_tags"
    );
    assert!(
        !allow.contains_key("low"),
        "level with empty allow should not be in allow_tags"
    );
    assert!(deny.is_empty());
    assert!(allow.is_empty());
}
