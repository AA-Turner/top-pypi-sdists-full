use crate::terminal_state::{TerminalStateContext, TerminalStateExtractor, UserBehaviorMetrics};
use std::time::Duration;

#[test]
fn test_terminal_state_extractor_new() {
    let extractor = TerminalStateExtractor::new();
    assert_eq!(extractor.command_count(), 0);
    assert_eq!(extractor.keystroke_count(), 0);
}

#[test]
fn test_record_command() {
    let mut extractor = TerminalStateExtractor::new();
    extractor.record_command("ls -la");
    assert_eq!(extractor.command_count(), 1);

    extractor.record_command("cd /tmp");
    assert_eq!(extractor.command_count(), 2);
    assert_eq!(extractor.navigation_history.len(), 1);
}

#[test]
fn test_record_keystroke() {
    let mut extractor = TerminalStateExtractor::new();
    extractor.record_keystroke(false);
    extractor.record_keystroke(false);
    extractor.record_keystroke(true); // backspace
    assert_eq!(extractor.keystroke_count(), 3);
    assert_eq!(extractor.correction_count, 1);
}

#[test]
#[cfg(feature = "terminal-state")]
fn test_parse_current_directory() {
    let extractor = TerminalStateExtractor::new();

    // Test user@host:/path$ format
    let screen = "user@host:/home/user$ ";
    let dir = extractor.parse_current_directory(screen);
    assert_eq!(dir, Some("/home/user".to_string()));

    // Test [/path] format
    let screen = "[/tmp] $ ";
    let dir = extractor.parse_current_directory(screen);
    assert_eq!(dir, Some("/tmp".to_string()));
}

#[test]
fn test_behavior_metrics_suspicious() {
    let metrics = UserBehaviorMetrics {
        session_duration: Duration::from_secs(120),
        command_rate: 35.0, // Too high
        avg_command_interval: Duration::from_secs(1),
        typing_speed: 15.0,
        correction_count: 0,
        navigation_pattern: vec![],
    };

    assert!(metrics.is_suspicious());
}

#[test]
fn test_behavior_metrics_confused() {
    let metrics = UserBehaviorMetrics {
        session_duration: Duration::from_secs(60),
        command_rate: 5.0,
        avg_command_interval: Duration::from_secs(10),
        typing_speed: 3.0,
        correction_count: 25, // Many corrections
        navigation_pattern: vec![],
    };

    assert!(metrics.is_confused());
}

#[test]
fn test_terminal_state_context_to_json() {
    let context = TerminalStateContext {
        command: "ls -la".to_string(),
        screen_contents: "$ ls -la\n".to_string(),
        current_directory: Some("/home/user".to_string()),
        cursor_position: (10, 5),
        command_history: vec!["pwd".to_string(), "cd /tmp".to_string()],
        recent_output: vec!["file1.txt".to_string(), "file2.txt".to_string()],
        scrollback: vec![],
        behavior: UserBehaviorMetrics {
            session_duration: Duration::from_secs(60),
            command_rate: 5.0,
            avg_command_interval: Duration::from_secs(10),
            typing_speed: 3.5,
            correction_count: 2,
            navigation_pattern: vec!["cd /tmp".to_string()],
        },
    };

    let json = context.to_json();
    assert_eq!(json["command"], "ls -la");
    assert_eq!(json["current_directory"], "/home/user");
    assert_eq!(json["behavior"]["command_rate"], 5.0);
}
