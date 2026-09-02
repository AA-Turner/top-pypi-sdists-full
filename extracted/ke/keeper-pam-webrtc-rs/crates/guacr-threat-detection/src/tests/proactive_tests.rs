use crate::approval::ApprovalManager;
use crate::command_buffer::CommandBuffer;
use crate::detector::{ThreatDetector, ThreatDetectorConfig};
use crate::proactive::{
    handle_proactive_input, parse_proactive_config, ProactiveResult, KEYSYM_BACKSPACE,
    KEYSYM_CTRL_C, KEYSYM_RETURN,
};
use std::collections::HashMap;
use std::sync::Arc;
use std::time::Duration;

#[tokio::test]
async fn test_proactive_input_empty_command() {
    let config = ThreatDetectorConfig::default();
    let detector = Arc::new(ThreatDetector::new(config).unwrap());
    let manager = ApprovalManager::new(detector, Duration::from_secs(5), false);
    let mut buffer = CommandBuffer::new();

    let result = handle_proactive_input(
        &mut buffer,
        b"\n",
        KEYSYM_RETURN,
        false,
        &manager,
        "session-1",
        "user",
        "host",
        "ssh",
        true,
    )
    .await;

    match result {
        ProactiveResult::Approved(_) => {
            assert!(buffer.is_empty());
        }
        _ => panic!("Expected Approved for empty command"),
    }
}

#[tokio::test]
async fn test_proactive_input_buffering() {
    let config = ThreatDetectorConfig::default();
    let detector = Arc::new(ThreatDetector::new(config).unwrap());
    let manager = ApprovalManager::new(detector, Duration::from_secs(5), false);
    let mut buffer = CommandBuffer::new();

    // Type "ls"
    let result = handle_proactive_input(
        &mut buffer,
        b"l",
        108, // 'l'
        false,
        &manager,
        "session-1",
        "user",
        "host",
        "ssh",
        true,
    )
    .await;

    match result {
        ProactiveResult::Approved(_) => {
            assert_eq!(buffer.as_str(), "l");
        }
        _ => panic!("Expected Approved for regular character"),
    }

    let result = handle_proactive_input(
        &mut buffer,
        b"s",
        115, // 's'
        false,
        &manager,
        "session-1",
        "user",
        "host",
        "ssh",
        true,
    )
    .await;

    match result {
        ProactiveResult::Approved(_) => {
            assert_eq!(buffer.as_str(), "ls");
        }
        _ => panic!("Expected Approved for regular character"),
    }
}

#[tokio::test]
async fn test_proactive_input_backspace() {
    let config = ThreatDetectorConfig::default();
    let detector = Arc::new(ThreatDetector::new(config).unwrap());
    let manager = ApprovalManager::new(detector, Duration::from_secs(5), false);
    let mut buffer = CommandBuffer::new();

    buffer.append_str("ls");

    let result = handle_proactive_input(
        &mut buffer,
        &[0x7f], // Backspace byte
        KEYSYM_BACKSPACE,
        false,
        &manager,
        "session-1",
        "user",
        "host",
        "ssh",
        true,
    )
    .await;

    match result {
        ProactiveResult::Approved(_) => {
            assert_eq!(buffer.as_str(), "l");
        }
        _ => panic!("Expected Approved for backspace"),
    }
}

#[tokio::test]
async fn test_proactive_input_ctrl_c() {
    let config = ThreatDetectorConfig::default();
    let detector = Arc::new(ThreatDetector::new(config).unwrap());
    let manager = ApprovalManager::new(detector, Duration::from_secs(5), false);
    let mut buffer = CommandBuffer::new();

    buffer.append_str("ls -la");

    let result = handle_proactive_input(
        &mut buffer,
        &[0x03], // Ctrl+C byte
        KEYSYM_CTRL_C,
        true,
        &manager,
        "session-1",
        "user",
        "host",
        "ssh",
        true,
    )
    .await;

    match result {
        ProactiveResult::Approved(_) => {
            assert!(buffer.is_empty());
        }
        _ => panic!("Expected Approved for Ctrl+C"),
    }
}

#[test]
fn test_parse_proactive_config() {
    let mut params = HashMap::new();
    params.insert(
        "threat_detection_proactive_mode".to_string(),
        "true".to_string(),
    );
    params.insert(
        "threat_detection_approval_timeout_ms".to_string(),
        "5000".to_string(),
    );
    params.insert(
        "threat_detection_fail_closed_on_error".to_string(),
        "true".to_string(),
    );

    let config = parse_proactive_config(&params);
    assert!(config.enabled);
    assert_eq!(config.approval_timeout_ms, 5000);
    assert!(config.fail_closed_on_error);
}
