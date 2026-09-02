use crate::ThreatDetector;
use std::sync::Arc;

/// RAII guard for automatic session cleanup
///
/// Ensures `cleanup_session()` is called when the guard is dropped,
/// preventing memory leaks from unbounded HashMap growth.
///
/// # Example
///
/// ```rust,no_run
/// use guacr_threat_detection::{ThreatDetector, ThreatDetectorConfig, SessionGuard};
/// use std::sync::Arc;
///
/// # async fn example() -> Result<(), Box<dyn std::error::Error>> {
/// let config = ThreatDetectorConfig::default();
/// let detector = Arc::new(ThreatDetector::new(config)?);
/// let session_id = uuid::Uuid::new_v4().to_string();
///
/// // Create guard - will cleanup on drop
/// let _guard = SessionGuard::new(detector.clone(), session_id.clone());
///
/// // Use detector...
/// detector.analyze_keystroke_sequence(&session_id, "ls", "user", "host", "ssh").await?;
///
/// // When guard drops (end of scope), cleanup_session() is called automatically
/// # Ok(())
/// # }
/// ```
pub struct SessionGuard {
    detector: Arc<ThreatDetector>,
    session_id: String,
}

impl SessionGuard {
    /// Create a new session guard
    ///
    /// The session will be automatically cleaned up when this guard is dropped.
    pub fn new(detector: Arc<ThreatDetector>, session_id: String) -> Self {
        Self {
            detector,
            session_id,
        }
    }

    /// Get the session ID
    pub fn session_id(&self) -> &str {
        &self.session_id
    }
}

impl Drop for SessionGuard {
    fn drop(&mut self) {
        // Cleanup session when guard is dropped
        self.detector.cleanup_session(&self.session_id);
    }
}
