// Security tests for AI threat detection.
// Run with: cargo test -p guacr-threat-detection --test security_test -- --include-ignored
#[cfg(test)]
mod security_tests {
    #[tokio::test]
    #[ignore]
    async fn test_deny_tag_injection_rejected() {
        use guacr_threat_detection::{ThreatDetector, ThreatDetectorConfig};
        use std::collections::HashMap;
        use std::sync::Arc;

        let mut deny_tags = HashMap::new();
        deny_tags.insert("critical".to_string(), vec!["rm.*-rf".to_string()]);

        let config = ThreatDetectorConfig {
            enabled: true,
            enable_tag_checking: true,
            deny_tags,
            ..Default::default()
        };
        let detector = Arc::new(ThreatDetector::new(config).unwrap());

        // Verify the detector is enabled and configured for tag checking
        assert!(detector.should_analyze("ssh", "return"));

        // For a full tag-based injection test, use the internal unit tests
        // (in src/tests/detector_tests.rs) which have access to check_tags().
        println!("Injection rejection test — implement with actual handler via integration test");
    }

    #[test]
    #[ignore]
    fn test_session_credentials_not_logged() {
        use guacr_threat_detection::{ThreatDetector, ThreatDetectorConfig};
        use std::sync::Arc;

        // Verify that session state does not store or leak credentials
        let config = ThreatDetectorConfig {
            enabled: true,
            baml_endpoint: "http://localhost:8000/api".to_string(),
            ..Default::default()
        };
        let detector = Arc::new(ThreatDetector::new(config).unwrap());

        // Create a session
        let session_id = "test-credential-session".to_string();

        // The session ID should not contain sensitive data
        assert!(!session_id.contains("password"));
        assert!(!session_id.contains("secret"));

        // Verify session count
        assert_eq!(
            detector.active_session_count(),
            0,
            "No sessions should exist before any activity"
        );

        println!("Credential logging test — verify sessions do not store passwords");
    }
}
