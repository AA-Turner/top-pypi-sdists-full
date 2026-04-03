use serde::{Deserialize, Serialize};
use std::collections::HashMap;

/// Threat level detected by AI
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum ThreatLevel {
    /// No threat detected
    None,
    /// Low risk - suspicious but not dangerous
    Low,
    /// Medium risk - potentially dangerous
    Medium,
    /// High risk - likely malicious
    High,
    /// Critical - immediate threat, terminate session
    Critical,
}

impl ThreatLevel {
    /// Convert a numeric risk score (0-20) to a ThreatLevel.
    ///
    /// Ranges:
    /// - 0     = None
    /// - 1-5   = Low
    /// - 6-10  = Medium
    /// - 11-15 = High
    /// - 16-20 = Critical
    pub fn from_risk_score(score: u8) -> Self {
        match score {
            0 => ThreatLevel::None,
            1..=5 => ThreatLevel::Low,
            6..=10 => ThreatLevel::Medium,
            11..=15 => ThreatLevel::High,
            16..=20 => ThreatLevel::Critical,
            // Scores above 20 are clamped to Critical
            _ => ThreatLevel::Critical,
        }
    }

    /// Convert this ThreatLevel to its midpoint risk score.
    ///
    /// Midpoints:
    /// - None     = 0
    /// - Low      = 3
    /// - Medium   = 8
    /// - High     = 13
    /// - Critical = 18
    pub fn to_risk_score(&self) -> u8 {
        match self {
            ThreatLevel::None => 0,
            ThreatLevel::Low => 3,
            ThreatLevel::Medium => 8,
            ThreatLevel::High => 13,
            ThreatLevel::Critical => 18,
        }
    }
}

/// Where a risk score originated from
#[derive(Debug, Default, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum RiskSource {
    /// Risk score from the LLM model (default)
    #[default]
    ModelDefault,
    /// Risk score from custom tag rule matching
    CustomTagRule,
    /// Risk score from local action effect classifier
    ActionEffectClassifier,
}

/// A single tag match result from deny/allow tag rule evaluation
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TagMatch {
    /// The regex pattern that matched
    pub tag: String,
    /// The risk level this tag is configured at (e.g., "critical", "high")
    pub level: String,
    /// "deny" or "allow"
    pub tag_type: String,
}

/// Collection of deny and allow tag matches from rule evaluation
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct TagMatches {
    pub deny_tags: Vec<TagMatch>,
    pub allow_tags: Vec<TagMatch>,
}

impl TagMatches {
    /// Returns true if any deny tags matched
    pub fn has_deny_tags(&self) -> bool {
        !self.deny_tags.is_empty()
    }

    /// Returns true if any allow tags matched
    pub fn has_allow_tags(&self) -> bool {
        !self.allow_tags.is_empty()
    }

    /// Returns true if allow tags matched but no deny tags did
    pub fn has_only_allow_tags(&self) -> bool {
        !self.allow_tags.is_empty() && self.deny_tags.is_empty()
    }
}

/// Threat detection result
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ThreatResult {
    /// Categorical threat level (backward compat)
    pub level: ThreatLevel,
    /// Numeric risk score (1-20), 0 means no threat
    pub risk_score: u8,
    /// Where the risk score came from
    #[serde(default)]
    pub risk_level_source: RiskSource,
    /// Confidence score (0.0 to 1.0)
    pub confidence: f64,
    /// Description of the threat (risk_category - reasoning)
    pub description: String,
    /// Recommended action
    pub action: String,
    /// The exact command text identified (if any)
    #[serde(default)]
    pub command_text: Option<String>,
    /// Risk category from analysis
    #[serde(default)]
    pub risk_category: Option<String>,
    /// Tag matches (deny/allow)
    #[serde(default)]
    pub tag_matches: TagMatches,
    /// Whether this result should trigger session termination
    /// (determined by termination gating logic, not just threat level)
    pub should_terminate_session: bool,
    /// Additional context/metadata
    #[serde(default)]
    pub metadata: serde_json::Value,
}

impl ThreatResult {
    pub fn is_threat(&self) -> bool {
        matches!(
            self.level,
            ThreatLevel::Low | ThreatLevel::Medium | ThreatLevel::High | ThreatLevel::Critical
        )
    }

    pub fn should_terminate(&self) -> bool {
        self.should_terminate_session
    }
}

impl Default for ThreatResult {
    fn default() -> Self {
        Self {
            level: ThreatLevel::None,
            risk_score: 0,
            risk_level_source: RiskSource::ModelDefault,
            confidence: 0.0,
            description: "No threat detected".to_string(),
            action: "continue".to_string(),
            command_text: None,
            risk_category: None,
            tag_matches: TagMatches::default(),
            should_terminate_session: false,
            metadata: serde_json::Value::Null,
        }
    }
}

/// Structured summary output from analysis, matching Python's AnalysisRecord
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AnalysisRecord {
    pub risk_score: u8,
    pub risk_level: String,
    pub risk_category: String,
    pub action_effects: String,
    pub command_text: Option<String>,
    pub overall_summary: String,
    pub risk_level_source: RiskSource,
    pub tag_matches: TagMatches,
    pub should_terminate: bool,
}

/// Termination policy configuration (matches Python's ai_settings hierarchy)
#[derive(Debug, Clone, Default, Serialize, Deserialize)]
pub struct TerminationPolicy {
    /// Global kill switch - if false, AI can NEVER terminate sessions
    pub config_allow_ai_session_terminate: bool,
    /// Per-resource enable - if false, this resource's sessions won't be terminated
    pub resource_ai_session_terminate_enabled: bool,
    /// Per-risk-level termination flags (e.g., "critical" -> true, "high" -> false)
    pub level_terminate_flags: HashMap<String, bool>,
}
