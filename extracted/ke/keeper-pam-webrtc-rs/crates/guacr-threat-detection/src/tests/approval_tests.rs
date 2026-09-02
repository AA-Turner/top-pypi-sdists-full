use crate::approval::{ApprovalDecision, ApprovalManager};
use crate::detector::{ThreatDetector, ThreatDetectorConfig};
use crate::threat::{ThreatLevel, ThreatResult};
use std::sync::Arc;
use std::time::Duration;

#[test]
fn test_approval_decision_from_threat_result() {
    let threat = ThreatResult {
        level: ThreatLevel::Critical,
        risk_score: ThreatLevel::Critical.to_risk_score(),
        confidence: 0.95,
        description: "Dangerous command".to_string(),
        action: "terminate".to_string(),
        should_terminate_session: true,
        metadata: serde_json::Value::Null,
        ..Default::default()
    };

    let decision = ApprovalDecision::from_threat_result(threat);
    assert!(decision.is_blocked());
}

#[test]
fn test_approval_decision_approved() {
    let threat = ThreatResult {
        level: ThreatLevel::Low,
        risk_score: ThreatLevel::Low.to_risk_score(),
        confidence: 0.1,
        description: "Safe command".to_string(),
        action: "continue".to_string(),
        should_terminate_session: false,
        metadata: serde_json::Value::Null,
        ..Default::default()
    };

    let decision = ApprovalDecision::from_threat_result(threat);
    assert!(decision.is_approved());
}

#[tokio::test]
async fn test_approval_manager_auto_approve() {
    let config = ThreatDetectorConfig::default();
    let detector = Arc::new(ThreatDetector::new(config).unwrap());
    let manager = ApprovalManager::new(detector, Duration::from_secs(5), false);

    assert!(manager.should_auto_approve("ls"));
    assert!(manager.should_auto_approve("ls -la"));
    assert!(manager.should_auto_approve("pwd"));
    assert!(manager.should_auto_approve("cd /tmp"));

    assert!(!manager.should_auto_approve("rm -rf /"));
    assert!(!manager.should_auto_approve("sudo rm"));
    assert!(!manager.should_auto_approve("lsblk")); // Not in safe list
}
