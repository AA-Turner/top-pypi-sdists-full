use crate::detector::{ThreatDetector, ThreatDetectorConfig};
use crate::session_guard::SessionGuard;
use std::sync::Arc;

#[tokio::test]
async fn test_session_guard_cleanup() {
    let config = ThreatDetectorConfig {
        enabled: true, // Enable detector
        baml_endpoint: "http://localhost:8000/api".to_string(),
        ..Default::default()
    };
    let detector = Arc::new(ThreatDetector::new(config).unwrap());
    let session_id = "test-session".to_string();

    // Initially no sessions
    assert_eq!(detector.active_session_count(), 0);

    {
        // Create guard
        let _guard = SessionGuard::new(detector.clone(), session_id.clone());

        // Add some history via public API (will fail to call BAML but will add to history)
        let _ = detector
            .analyze_keystroke_sequence(&session_id, "ls", "user", "host", "ssh")
            .await;

        // History should be created (even if BAML call failed)
        assert_eq!(detector.active_session_count(), 1);

        // Guard will drop here
    }

    // Session should be cleaned up
    assert_eq!(detector.active_session_count(), 0);
}
