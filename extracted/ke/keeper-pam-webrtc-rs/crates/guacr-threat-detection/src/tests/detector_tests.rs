use crate::detector::{should_trigger_analysis, ThreatDetector, ThreatDetectorConfig};
use crate::threat::{TagMatch, TagMatches, ThreatLevel, ThreatResult};
use crate::RiskSource;
use std::collections::HashMap;

#[test]
fn test_threat_detector_config_default() {
    let config = ThreatDetectorConfig::default();
    assert!(!config.enabled);
    assert!(config.auto_terminate);
    assert!(config.config_allow_ai_session_terminate);
    assert!(config.resource_ai_session_terminate_enabled);
    assert!(config.level_terminate_flags.is_empty());
}

#[test]
fn test_should_terminate() {
    let config = ThreatDetectorConfig {
        enabled: true,
        auto_terminate: true,
        ..Default::default()
    };
    let detector = ThreatDetector::new(config).unwrap();

    let critical_threat = ThreatResult {
        level: ThreatLevel::Critical,
        risk_score: 18,
        risk_level_source: RiskSource::ModelDefault,
        confidence: 0.95,
        description: "Critical threat".to_string(),
        action: "terminate".to_string(),
        command_text: None,
        risk_category: None,
        tag_matches: TagMatches::default(),
        should_terminate_session: true,
        metadata: serde_json::Value::Null,
    };

    assert!(detector.should_terminate(&critical_threat));

    let safe_result = ThreatResult::default();
    assert!(!detector.should_terminate(&safe_result));
}

#[test]
fn test_should_trigger_analysis_ssh() {
    assert!(should_trigger_analysis("ssh", "return"));
    assert!(!should_trigger_analysis("ssh", "click"));
    assert!(!should_trigger_analysis("ssh", "escape"));
}

#[test]
fn test_should_trigger_analysis_rdp() {
    assert!(should_trigger_analysis("rdp", "return"));
    assert!(should_trigger_analysis("rdp", "click"));
    assert!(should_trigger_analysis("rdp", "escape"));
    assert!(!should_trigger_analysis("rdp", "tab"));
}

#[test]
fn test_should_trigger_analysis_http() {
    assert!(should_trigger_analysis("http", "return"));
    assert!(should_trigger_analysis("http", "click"));
    assert!(!should_trigger_analysis("http", "escape"));
}

#[test]
fn test_should_trigger_analysis_unknown_protocol() {
    assert!(should_trigger_analysis("unknown", "return"));
    assert!(!should_trigger_analysis("unknown", "click"));
}

#[test]
fn test_should_analyze_disabled() {
    let config = ThreatDetectorConfig {
        enabled: false,
        ..Default::default()
    };
    let detector = ThreatDetector::new(config).unwrap();
    assert!(!detector.should_analyze("ssh", "return"));
}

#[test]
fn test_should_analyze_enabled() {
    let config = ThreatDetectorConfig {
        enabled: true,
        ..Default::default()
    };
    let detector = ThreatDetector::new(config).unwrap();
    assert!(detector.should_analyze("ssh", "return"));
    assert!(!detector.should_analyze("ssh", "click"));
    assert!(detector.should_analyze("rdp", "click"));
}

#[test]
fn test_check_tags_deny_collects_all_matches() {
    let mut deny_tags = HashMap::new();
    deny_tags.insert("critical".to_string(), vec!["rm.*-rf".to_string()]);
    deny_tags.insert("high".to_string(), vec!["rm".to_string()]);

    let config = ThreatDetectorConfig {
        enabled: true,
        enable_tag_checking: true,
        deny_tags,
        ..Default::default()
    };
    let detector = ThreatDetector::new(config).unwrap();

    let result = detector.check_tags("rm -rf /");

    // Both deny tags should match
    assert_eq!(result.deny_matches.len(), 2);
    assert!(result.threat.is_some());

    let threat = result.threat.unwrap();
    // Should use the highest level (Critical)
    assert_eq!(threat.level, ThreatLevel::Critical);
    assert_eq!(threat.risk_level_source, RiskSource::CustomTagRule);
    assert_eq!(threat.confidence, 1.0);
}

#[test]
fn test_check_tags_allow_only() {
    let mut allow_tags = HashMap::new();
    allow_tags.insert("low".to_string(), vec!["^ls".to_string()]);

    let config = ThreatDetectorConfig {
        enabled: true,
        enable_tag_checking: true,
        allow_tags,
        ..Default::default()
    };
    let detector = ThreatDetector::new(config).unwrap();

    let result = detector.check_tags("ls -la");

    assert!(result.threat.is_none());
    assert!(result.deny_matches.is_empty());
    assert_eq!(result.allow_matches.len(), 1);
    assert_eq!(result.allow_matches[0].tag_type, "allow");
}

#[test]
fn test_check_tags_no_matches() {
    let config = ThreatDetectorConfig {
        enabled: true,
        enable_tag_checking: true,
        ..Default::default()
    };
    let detector = ThreatDetector::new(config).unwrap();

    let result = detector.check_tags("echo hello");

    assert!(result.threat.is_none());
    assert!(result.deny_matches.is_empty());
    assert!(result.allow_matches.is_empty());
}

#[test]
fn test_check_tags_disabled() {
    let mut deny_tags = HashMap::new();
    deny_tags.insert("critical".to_string(), vec!["rm".to_string()]);

    let config = ThreatDetectorConfig {
        enabled: true,
        enable_tag_checking: false,
        deny_tags,
        ..Default::default()
    };
    let detector = ThreatDetector::new(config).unwrap();

    let result = detector.check_tags("rm -rf /");

    // Tag checking disabled, so no matches
    assert!(result.threat.is_none());
    assert!(result.deny_matches.is_empty());
}

#[test]
fn test_determine_should_terminate_global_gate() {
    let config = ThreatDetectorConfig {
        enabled: true,
        config_allow_ai_session_terminate: false,
        ..Default::default()
    };
    let detector = ThreatDetector::new(config).unwrap();

    let threat = ThreatResult {
        level: ThreatLevel::Critical,
        risk_score: 18,
        should_terminate_session: false,
        ..Default::default()
    };

    // Global gate is off, so should never terminate
    assert!(!detector.determine_should_terminate(&threat));
}

#[test]
fn test_determine_should_terminate_resource_gate() {
    let config = ThreatDetectorConfig {
        enabled: true,
        config_allow_ai_session_terminate: true,
        resource_ai_session_terminate_enabled: false,
        ..Default::default()
    };
    let detector = ThreatDetector::new(config).unwrap();

    let threat = ThreatResult {
        level: ThreatLevel::Critical,
        risk_score: 18,
        should_terminate_session: false,
        ..Default::default()
    };

    // Resource gate is off, so should never terminate
    assert!(!detector.determine_should_terminate(&threat));
}

#[test]
fn test_determine_should_terminate_deny_tags_always() {
    let config = ThreatDetectorConfig {
        enabled: true,
        config_allow_ai_session_terminate: true,
        resource_ai_session_terminate_enabled: true,
        ..Default::default()
    };
    let detector = ThreatDetector::new(config).unwrap();

    let threat = ThreatResult {
        level: ThreatLevel::Low, // Even low level
        risk_score: 3,
        tag_matches: TagMatches {
            deny_tags: vec![TagMatch {
                tag: "rm".to_string(),
                level: "low".to_string(),
                tag_type: "deny".to_string(),
            }],
            allow_tags: vec![],
        },
        should_terminate_session: false,
        ..Default::default()
    };

    // Deny tags always terminate (regardless of level)
    assert!(detector.determine_should_terminate(&threat));
}

#[test]
fn test_determine_should_terminate_allow_only_never() {
    let config = ThreatDetectorConfig {
        enabled: true,
        config_allow_ai_session_terminate: true,
        resource_ai_session_terminate_enabled: true,
        ..Default::default()
    };
    let detector = ThreatDetector::new(config).unwrap();

    let threat = ThreatResult {
        level: ThreatLevel::High, // Even high level
        risk_score: 13,
        tag_matches: TagMatches {
            deny_tags: vec![],
            allow_tags: vec![TagMatch {
                tag: "ls".to_string(),
                level: "low".to_string(),
                tag_type: "allow".to_string(),
            }],
        },
        should_terminate_session: false,
        ..Default::default()
    };

    // Allow-only tags never terminate
    assert!(!detector.determine_should_terminate(&threat));
}

#[test]
fn test_determine_should_terminate_level_flags() {
    let mut level_flags = HashMap::new();
    level_flags.insert("medium".to_string(), true);
    level_flags.insert("high".to_string(), false);

    let config = ThreatDetectorConfig {
        enabled: true,
        config_allow_ai_session_terminate: true,
        resource_ai_session_terminate_enabled: true,
        level_terminate_flags: level_flags,
        ..Default::default()
    };
    let detector = ThreatDetector::new(config).unwrap();

    // Medium should terminate (per flag)
    let medium_threat = ThreatResult {
        level: ThreatLevel::Medium,
        risk_score: 8,
        ..Default::default()
    };
    assert!(detector.determine_should_terminate(&medium_threat));

    // High should NOT terminate (per flag, overriding default)
    let high_threat = ThreatResult {
        level: ThreatLevel::High,
        risk_score: 13,
        ..Default::default()
    };
    assert!(!detector.determine_should_terminate(&high_threat));
}

#[test]
fn test_determine_should_terminate_default_behavior() {
    let config = ThreatDetectorConfig {
        enabled: true,
        config_allow_ai_session_terminate: true,
        resource_ai_session_terminate_enabled: true,
        ..Default::default()
    };
    let detector = ThreatDetector::new(config).unwrap();

    // No level flags set, defaults apply
    assert!(!detector.determine_should_terminate(&ThreatResult {
        level: ThreatLevel::None,
        ..Default::default()
    }));
    assert!(!detector.determine_should_terminate(&ThreatResult {
        level: ThreatLevel::Low,
        ..Default::default()
    }));
    assert!(!detector.determine_should_terminate(&ThreatResult {
        level: ThreatLevel::Medium,
        ..Default::default()
    }));
    assert!(detector.determine_should_terminate(&ThreatResult {
        level: ThreatLevel::High,
        ..Default::default()
    }));
    assert!(detector.determine_should_terminate(&ThreatResult {
        level: ThreatLevel::Critical,
        ..Default::default()
    }));
}

#[test]
fn test_session_state_lifecycle() {
    use crate::detector::SessionState;

    let config = ThreatDetectorConfig {
        enabled: true,
        ..Default::default()
    };
    let detector = ThreatDetector::new(config).unwrap();

    assert_eq!(detector.active_session_count(), 0);

    // Manually insert a session state to test cleanup
    {
        let mut sessions = detector.sessions.write();
        sessions.insert("test-session".to_string(), SessionState::new());
    }

    assert_eq!(detector.active_session_count(), 1);

    detector.cleanup_session("test-session");
    assert_eq!(detector.active_session_count(), 0);
}

#[test]
fn test_get_command_sequence_with_session_state() {
    use crate::detector::SessionState;

    let config = ThreatDetectorConfig {
        enabled: true,
        ..Default::default()
    };
    let detector = ThreatDetector::new(config).unwrap();

    // No session yet
    assert!(detector.get_command_sequence("test-session").is_empty());

    // Insert session with commands
    {
        let mut sessions = detector.sessions.write();
        let mut state = SessionState::new();
        state.command_history.push_back("ls".to_string());
        state.command_history.push_back("pwd".to_string());
        sessions.insert("test-session".to_string(), state);
    }

    let cmds = detector.get_command_sequence("test-session");
    assert_eq!(cmds.len(), 2);
    assert_eq!(cmds[0], "ls");
    assert_eq!(cmds[1], "pwd");
}

#[test]
fn test_cleanup_nonexistent_session() {
    let config = ThreatDetectorConfig {
        enabled: true,
        ..Default::default()
    };
    let detector = ThreatDetector::new(config).unwrap();

    // Should not panic
    detector.cleanup_session("nonexistent");
    assert_eq!(detector.active_session_count(), 0);
}

#[test]
fn test_session_state_new() {
    use crate::detector::SessionState;
    let state = SessionState::new();
    assert!(state.command_history.is_empty());
    assert!(state.processed_commands.is_empty());
    assert!(state.is_first_interaction);
}
