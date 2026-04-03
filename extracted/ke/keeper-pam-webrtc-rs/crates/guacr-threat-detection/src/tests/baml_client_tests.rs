use crate::baml_client::{Analysis, BamlClient, CommandSummaryResponse};
use crate::threat::{RiskSource, ThreatLevel};
use crate::{Result, ThreatDetectionError};

/// Helper to create an Analysis with all fields for testing
fn make_analysis(risk_level: &str, risk_category: &str, reasoning: &str) -> Analysis {
    Analysis {
        risk_level: risk_level.to_string(),
        risk_score: None,
        risk_category: risk_category.to_string(),
        action_effects: None,
        command_text: None,
        reasoning: reasoning.to_string(),
        overall_summary: None,
    }
}

#[test]
fn test_analysis_to_threat_result_critical() {
    let client = BamlClient::new("http://localhost:8000".to_string(), None, None);
    let analysis = make_analysis("Critical", "DestructiveActivity", "Command deletes files");

    let threat = client.analysis_to_threat_result(&analysis, "User deleted files");
    assert_eq!(threat.level, ThreatLevel::Critical);
    assert!(threat.should_terminate_session);
    assert_eq!(threat.action, "terminate");
    assert!(matches!(threat.risk_level_source, RiskSource::ModelDefault));
}

#[test]
fn test_analysis_to_threat_result_low() {
    let client = BamlClient::new("http://localhost:8000".to_string(), None, None);
    let analysis = make_analysis("Low", "RoutineOperations", "Lists directory contents");

    let threat = client.analysis_to_threat_result(&analysis, "User listed files");
    assert_eq!(threat.level, ThreatLevel::Low);
    assert!(!threat.should_terminate_session);
    assert_eq!(threat.action, "monitor");
}

#[test]
fn test_analysis_to_threat_result_with_risk_score() {
    let client = BamlClient::new("http://localhost:8000".to_string(), None, None);
    let analysis = Analysis {
        risk_level: "High".to_string(),
        risk_score: Some(16),
        risk_category: "DataExfiltration".to_string(),
        action_effects: Some("Copies sensitive data to external server".to_string()),
        command_text: Some("scp /etc/passwd remote:".to_string()),
        reasoning: "Exfiltrating sensitive system files".to_string(),
        overall_summary: Some("Data exfiltration attempt".to_string()),
    };

    let threat = client.analysis_to_threat_result(&analysis, "Data exfiltration detected");
    assert_eq!(threat.level, ThreatLevel::High);
    assert_eq!(threat.risk_score, 16);
    assert!(threat.should_terminate_session);
    assert_eq!(
        threat.command_text,
        Some("scp /etc/passwd remote:".to_string())
    );
    assert_eq!(threat.risk_category, Some("DataExfiltration".to_string()));
}

#[test]
fn test_analysis_to_threat_result_unknown_level() {
    let client = BamlClient::new("http://localhost:8000".to_string(), None, None);
    let analysis = make_analysis("Unknown", "Other", "Unrecognized risk level");

    let threat = client.analysis_to_threat_result(&analysis, "Unknown activity");
    assert_eq!(threat.level, ThreatLevel::None);
    assert!(!threat.should_terminate_session);
    assert_eq!(threat.action, "monitor");
}

#[test]
fn test_analysis_deserialization_with_all_fields() {
    let json = r#"{
        "risk_level": "High",
        "risk_score": 15,
        "risk_category": "DataExfiltration",
        "action_effects": "Copies files to remote server",
        "command_text": "scp data.db remote:",
        "reasoning": "Sensitive data transfer",
        "overall_summary": "User attempted data exfiltration"
    }"#;

    let analysis: Analysis = serde_json::from_str(json).unwrap();
    assert_eq!(analysis.risk_level, "High");
    assert_eq!(analysis.risk_score, Some(15));
    assert_eq!(analysis.risk_category, "DataExfiltration");
    assert_eq!(
        analysis.action_effects.as_deref(),
        Some("Copies files to remote server")
    );
    assert_eq!(
        analysis.command_text.as_deref(),
        Some("scp data.db remote:")
    );
    assert_eq!(analysis.reasoning, "Sensitive data transfer");
    assert_eq!(
        analysis.overall_summary.as_deref(),
        Some("User attempted data exfiltration")
    );
}

#[test]
fn test_analysis_deserialization_backward_compat() {
    // Old BAML responses only have risk_level, risk_category, reasoning
    let json = r#"{
        "risk_level": "Low",
        "risk_category": "RoutineOperations",
        "reasoning": "Lists directory"
    }"#;

    let analysis: Analysis = serde_json::from_str(json).unwrap();
    assert_eq!(analysis.risk_level, "Low");
    assert_eq!(analysis.risk_score, None);
    assert_eq!(analysis.risk_category, "RoutineOperations");
    assert_eq!(analysis.action_effects, None);
    assert_eq!(analysis.command_text, None);
    assert_eq!(analysis.reasoning, "Lists directory");
    assert_eq!(analysis.overall_summary, None);
}

#[test]
fn test_command_summary_response_deserialization() {
    let json = r#"{
        "overall_summary": "User performed routine operations",
        "overall_risk_score": 3,
        "overall_risk_level": "Low"
    }"#;

    let response: CommandSummaryResponse = serde_json::from_str(json).unwrap();
    assert_eq!(
        response.overall_summary,
        "User performed routine operations"
    );
    assert_eq!(response.overall_risk_score, Some(3));
    assert_eq!(response.overall_risk_level.as_deref(), Some("Low"));
}

#[test]
fn test_command_summary_response_backward_compat() {
    let json = r#"{
        "overall_summary": "User performed routine operations"
    }"#;

    let response: CommandSummaryResponse = serde_json::from_str(json).unwrap();
    assert_eq!(
        response.overall_summary,
        "User performed routine operations"
    );
    assert_eq!(response.overall_risk_score, None);
    assert_eq!(response.overall_risk_level, None);
}

#[tokio::test]
async fn test_retry_request_succeeds_first_try() {
    let client = BamlClient::new("http://localhost:8000".to_string(), None, None);
    let call_count = std::sync::atomic::AtomicU32::new(0);

    let result = client
        .retry_request(|| {
            call_count.fetch_add(1, std::sync::atomic::Ordering::SeqCst);
            async { Ok::<_, ThreatDetectionError>(42) }
        })
        .await;

    assert_eq!(result.unwrap(), 42);
    assert_eq!(call_count.load(std::sync::atomic::Ordering::SeqCst), 1);
}

#[tokio::test]
async fn test_retry_request_retries_on_failure() {
    let client = BamlClient::new("http://localhost:8000".to_string(), None, None);
    let call_count = std::sync::atomic::AtomicU32::new(0);

    let result = client
        .retry_request(|| {
            let attempt = call_count.fetch_add(1, std::sync::atomic::Ordering::SeqCst);
            async move {
                if attempt < 2 {
                    Err(ThreatDetectionError::BamlApiError(
                        "transient failure".to_string(),
                    ))
                } else {
                    Ok::<_, ThreatDetectionError>(99)
                }
            }
        })
        .await;

    assert_eq!(result.unwrap(), 99);
    // Should have been called 3 times: 2 failures + 1 success
    assert_eq!(call_count.load(std::sync::atomic::Ordering::SeqCst), 3);
}

#[tokio::test]
async fn test_retry_request_exhausts_retries() {
    use crate::baml_client::MAX_RETRIES;

    let client = BamlClient::new("http://localhost:8000".to_string(), None, None);
    let call_count = std::sync::atomic::AtomicU32::new(0);

    let result: Result<i32> = client
        .retry_request(|| {
            call_count.fetch_add(1, std::sync::atomic::Ordering::SeqCst);
            async {
                Err(ThreatDetectionError::BamlApiError(
                    "persistent failure".to_string(),
                ))
            }
        })
        .await;

    assert!(result.is_err());
    // MAX_RETRIES + 1 = 4 attempts total
    assert_eq!(
        call_count.load(std::sync::atomic::Ordering::SeqCst),
        MAX_RETRIES + 1
    );
}

#[test]
fn test_analysis_serialization_roundtrip() {
    let analysis = Analysis {
        risk_level: "High".to_string(),
        risk_score: Some(15),
        risk_category: "DataExfiltration".to_string(),
        action_effects: Some("Copies files".to_string()),
        command_text: Some("scp data remote:".to_string()),
        reasoning: "Sensitive transfer".to_string(),
        overall_summary: Some("Exfiltration attempt".to_string()),
    };

    let json = serde_json::to_string(&analysis).unwrap();
    let deserialized: Analysis = serde_json::from_str(&json).unwrap();

    assert_eq!(deserialized.risk_level, analysis.risk_level);
    assert_eq!(deserialized.risk_score, analysis.risk_score);
    assert_eq!(deserialized.risk_category, analysis.risk_category);
    assert_eq!(deserialized.action_effects, analysis.action_effects);
    assert_eq!(deserialized.command_text, analysis.command_text);
    assert_eq!(deserialized.reasoning, analysis.reasoning);
    assert_eq!(deserialized.overall_summary, analysis.overall_summary);
}
