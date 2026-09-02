use crate::threat::{
    AnalysisRecord, RiskSource, TagMatch, TagMatches, TerminationPolicy, ThreatLevel, ThreatResult,
};

#[test]
fn test_threat_level_from_risk_score_none() {
    assert_eq!(ThreatLevel::from_risk_score(0), ThreatLevel::None);
}

#[test]
fn test_threat_level_from_risk_score_low() {
    assert_eq!(ThreatLevel::from_risk_score(1), ThreatLevel::Low);
    assert_eq!(ThreatLevel::from_risk_score(3), ThreatLevel::Low);
    assert_eq!(ThreatLevel::from_risk_score(5), ThreatLevel::Low);
}

#[test]
fn test_threat_level_from_risk_score_medium() {
    assert_eq!(ThreatLevel::from_risk_score(6), ThreatLevel::Medium);
    assert_eq!(ThreatLevel::from_risk_score(8), ThreatLevel::Medium);
    assert_eq!(ThreatLevel::from_risk_score(10), ThreatLevel::Medium);
}

#[test]
fn test_threat_level_from_risk_score_high() {
    assert_eq!(ThreatLevel::from_risk_score(11), ThreatLevel::High);
    assert_eq!(ThreatLevel::from_risk_score(13), ThreatLevel::High);
    assert_eq!(ThreatLevel::from_risk_score(15), ThreatLevel::High);
}

#[test]
fn test_threat_level_from_risk_score_critical() {
    assert_eq!(ThreatLevel::from_risk_score(16), ThreatLevel::Critical);
    assert_eq!(ThreatLevel::from_risk_score(18), ThreatLevel::Critical);
    assert_eq!(ThreatLevel::from_risk_score(20), ThreatLevel::Critical);
}

#[test]
fn test_threat_level_from_risk_score_above_max() {
    // Scores above 20 should clamp to Critical
    assert_eq!(ThreatLevel::from_risk_score(21), ThreatLevel::Critical);
    assert_eq!(ThreatLevel::from_risk_score(255), ThreatLevel::Critical);
}

#[test]
fn test_threat_level_to_risk_score_midpoints() {
    assert_eq!(ThreatLevel::None.to_risk_score(), 0);
    assert_eq!(ThreatLevel::Low.to_risk_score(), 3);
    assert_eq!(ThreatLevel::Medium.to_risk_score(), 8);
    assert_eq!(ThreatLevel::High.to_risk_score(), 13);
    assert_eq!(ThreatLevel::Critical.to_risk_score(), 18);
}

#[test]
fn test_threat_level_roundtrip() {
    // Converting to midpoint risk score and back should yield the same level
    for level in [
        ThreatLevel::None,
        ThreatLevel::Low,
        ThreatLevel::Medium,
        ThreatLevel::High,
        ThreatLevel::Critical,
    ] {
        let score = level.to_risk_score();
        let roundtripped = ThreatLevel::from_risk_score(score);
        assert_eq!(level, roundtripped, "Roundtrip failed for {:?}", level);
    }
}

#[test]
fn test_threat_level_ordering() {
    assert!(ThreatLevel::None < ThreatLevel::Low);
    assert!(ThreatLevel::Low < ThreatLevel::Medium);
    assert!(ThreatLevel::Medium < ThreatLevel::High);
    assert!(ThreatLevel::High < ThreatLevel::Critical);
}

#[test]
fn test_threat_result_default() {
    let result = ThreatResult::default();
    assert_eq!(result.level, ThreatLevel::None);
    assert_eq!(result.risk_score, 0);
    assert_eq!(result.risk_level_source, RiskSource::ModelDefault);
    assert_eq!(result.confidence, 0.0);
    assert!(!result.is_threat());
    assert!(!result.should_terminate());
    assert!(result.command_text.is_none());
    assert!(result.risk_category.is_none());
    assert!(!result.tag_matches.has_deny_tags());
    assert!(!result.tag_matches.has_allow_tags());
    assert!(!result.should_terminate_session);
}

#[test]
fn test_threat_result_is_threat() {
    let mut result = ThreatResult::default();
    assert!(!result.is_threat());

    result.level = ThreatLevel::Low;
    assert!(result.is_threat());

    result.level = ThreatLevel::Critical;
    assert!(result.is_threat());
}

#[test]
fn test_threat_result_should_terminate_uses_field() {
    let result = ThreatResult {
        level: ThreatLevel::Critical,
        ..Default::default()
    };
    // Even with Critical level, should_terminate returns false unless the field is set
    assert!(!result.should_terminate());

    let result = ThreatResult {
        level: ThreatLevel::Critical,
        should_terminate_session: true,
        ..Default::default()
    };
    assert!(result.should_terminate());
}

#[test]
fn test_risk_source_default() {
    assert_eq!(RiskSource::default(), RiskSource::ModelDefault);
}

#[test]
fn test_tag_matches_empty() {
    let matches = TagMatches::default();
    assert!(!matches.has_deny_tags());
    assert!(!matches.has_allow_tags());
    assert!(!matches.has_only_allow_tags());
}

#[test]
fn test_tag_matches_with_deny() {
    let matches = TagMatches {
        deny_tags: vec![TagMatch {
            tag: "rm -rf".to_string(),
            level: "critical".to_string(),
            tag_type: "deny".to_string(),
        }],
        allow_tags: vec![],
    };
    assert!(matches.has_deny_tags());
    assert!(!matches.has_allow_tags());
    assert!(!matches.has_only_allow_tags());
}

#[test]
fn test_tag_matches_with_allow_only() {
    let matches = TagMatches {
        deny_tags: vec![],
        allow_tags: vec![TagMatch {
            tag: "ls".to_string(),
            level: "low".to_string(),
            tag_type: "allow".to_string(),
        }],
    };
    assert!(!matches.has_deny_tags());
    assert!(matches.has_allow_tags());
    assert!(matches.has_only_allow_tags());
}

#[test]
fn test_tag_matches_with_both() {
    let matches = TagMatches {
        deny_tags: vec![TagMatch {
            tag: "rm".to_string(),
            level: "high".to_string(),
            tag_type: "deny".to_string(),
        }],
        allow_tags: vec![TagMatch {
            tag: "ls".to_string(),
            level: "low".to_string(),
            tag_type: "allow".to_string(),
        }],
    };
    assert!(matches.has_deny_tags());
    assert!(matches.has_allow_tags());
    assert!(!matches.has_only_allow_tags());
}

#[test]
fn test_threat_result_serialization_roundtrip() {
    let result = ThreatResult {
        level: ThreatLevel::High,
        risk_score: 13,
        risk_level_source: RiskSource::CustomTagRule,
        confidence: 0.95,
        description: "Destructive command detected".to_string(),
        action: "terminate".to_string(),
        command_text: Some("rm -rf /".to_string()),
        risk_category: Some("DestructiveActivity".to_string()),
        tag_matches: TagMatches {
            deny_tags: vec![TagMatch {
                tag: "rm.*-rf".to_string(),
                level: "critical".to_string(),
                tag_type: "deny".to_string(),
            }],
            allow_tags: vec![],
        },
        should_terminate_session: true,
        metadata: serde_json::json!({"source": "tag_rule"}),
    };

    let json = serde_json::to_string(&result).expect("serialization failed");
    let deserialized: ThreatResult = serde_json::from_str(&json).expect("deserialization failed");

    assert_eq!(deserialized.level, ThreatLevel::High);
    assert_eq!(deserialized.risk_score, 13);
    assert_eq!(deserialized.risk_level_source, RiskSource::CustomTagRule);
    assert_eq!(deserialized.confidence, 0.95);
    assert!(deserialized.should_terminate_session);
    assert_eq!(deserialized.command_text, Some("rm -rf /".to_string()));
    assert!(deserialized.tag_matches.has_deny_tags());
}

#[test]
fn test_threat_result_deserialization_missing_optional_fields() {
    // Simulate JSON from an older producer that only has the original fields
    let json = r#"{
        "level": "high",
        "confidence": 0.9,
        "description": "test threat",
        "action": "terminate",
        "risk_score": 13,
        "should_terminate_session": true,
        "metadata": null
    }"#;

    let result: ThreatResult = serde_json::from_str(json).expect("deserialization failed");
    assert_eq!(result.level, ThreatLevel::High);
    assert_eq!(result.risk_level_source, RiskSource::ModelDefault); // default
    assert!(result.command_text.is_none()); // default
    assert!(result.risk_category.is_none()); // default
    assert!(!result.tag_matches.has_deny_tags()); // default empty
}

#[test]
fn test_termination_policy_default() {
    let policy = TerminationPolicy::default();
    assert!(!policy.config_allow_ai_session_terminate);
    assert!(!policy.resource_ai_session_terminate_enabled);
    assert!(policy.level_terminate_flags.is_empty());
}

#[test]
fn test_analysis_record_serialization() {
    let record = AnalysisRecord {
        risk_score: 18,
        risk_level: "critical".to_string(),
        risk_category: "DestructiveActivity".to_string(),
        action_effects: "Deletes all files on system".to_string(),
        command_text: Some("rm -rf /".to_string()),
        overall_summary: "User attempted destructive command".to_string(),
        risk_level_source: RiskSource::ModelDefault,
        tag_matches: TagMatches::default(),
        should_terminate: true,
    };

    let json = serde_json::to_string(&record).expect("serialization failed");
    let deserialized: AnalysisRecord = serde_json::from_str(&json).expect("deserialization failed");

    assert_eq!(deserialized.risk_score, 18);
    assert_eq!(deserialized.risk_level, "critical");
    assert!(deserialized.should_terminate);
}
