use crate::threat::{RiskSource, TagMatches, ThreatLevel, ThreatResult};
use crate::{Result, ThreatDetectionError};
use log::{debug, error, warn};
use serde::{Deserialize, Serialize};
use std::time::Duration;

/// Retry configuration for BAML API calls
pub(crate) const MAX_RETRIES: u32 = 3;
const INITIAL_DELAY_MS: u64 = 200;
const BACKOFF_MULTIPLIER: f64 = 1.5;
const MAX_DELAY_MS: u64 = 10_000;

/// BAML REST API client for threat detection
///
/// Calls BAML REST API endpoint to analyze commands/activity for threats.
/// Based on BAML documentation: https://docs.boundaryml.com/guide/installation-language/rest-api-other-languages
///
/// Uses BAML functions:
/// - AnalyzeCliText: Analyze CLI text with protocol context and command history
/// - ExtractCommandSummary: Generate session summaries
///
/// All API calls are retried with exponential backoff on transient failures.
pub struct BamlClient {
    endpoint: String,
    api_key: Option<String>,
    client: reqwest::Client,
}

/// BAML function request payload for AnalyzeCliText
#[derive(Debug, Serialize)]
struct AnalyzeCliTextRequest {
    cli_lines: Vec<String>,
    previous_protocol: String,
    previous_commands: Vec<String>,
}

/// BAML function request payload for AnalyzeScreenshot
#[derive(Debug, Serialize)]
struct AnalyzeScreenshotRequest {
    /// Base64-encoded grayscale JPEG of the current screen.
    image_b64: String,
    /// Keystrokes buffered since the last trigger event, for context.
    buffered_keystrokes: String,
    /// Session identifier (for logging, not stored by BAML).
    session_id: String,
}

/// BAML function request payload for ExtractCommandSummary
#[derive(Debug, Serialize)]
struct ExtractCommandSummaryRequest {
    command_sequence: Vec<String>,
}

/// BAML KeystrokeAnalysisResponse (matches BAML schema)
#[derive(Debug, Deserialize, Serialize, Clone)]
pub struct KeystrokeAnalysisResponse {
    pub analysis_report: Vec<Analysis>,
    pub overall_summary: String,
}

/// BAML Analysis (matches BAML schema)
///
/// Contains both categorical risk_level and optional numeric risk_score (1-20).
/// New optional fields (risk_score, action_effects, command_text, overall_summary)
/// use `#[serde(default)]` for backward compatibility with older BAML responses.
#[derive(Debug, Deserialize, Clone, Serialize)]
pub struct Analysis {
    /// Categorical risk level string ("Low", "Medium", "High", "Critical")
    pub risk_level: String,
    /// Numeric risk score (1-20) - primary scoring, optional for backward compat
    #[serde(default)]
    pub risk_score: Option<u8>,
    /// Risk category (e.g., "DestructiveActivity", "DataExfiltration")
    pub risk_category: String,
    /// Factual description of what the command does
    #[serde(default)]
    pub action_effects: Option<String>,
    /// The exact command text identified by the LLM
    #[serde(default)]
    pub command_text: Option<String>,
    /// One sentence explanation of risk assessment
    pub reasoning: String,
    /// Brief summary ("The user performed...")
    #[serde(default)]
    pub overall_summary: Option<String>,
}

/// BAML CommandSummaryResponse (matches BAML schema)
#[derive(Debug, Deserialize, Serialize, Clone)]
pub struct CommandSummaryResponse {
    pub overall_summary: String,
    /// Overall risk score for the session (highest seen)
    #[serde(default)]
    pub overall_risk_score: Option<u8>,
    /// Overall risk level for the session
    #[serde(default)]
    pub overall_risk_level: Option<String>,
}

impl BamlClient {
    /// Create a new BAML client
    ///
    /// # Arguments
    ///
    /// * `endpoint` - BAML REST API endpoint URL
    /// * `api_key` - Optional API key for authentication
    /// * `timeout` - Request timeout (default: 5 seconds)
    pub fn new(endpoint: String, api_key: Option<String>, timeout: Option<Duration>) -> Self {
        // reqwest::Client::builder().build() only fails if TLS backend
        // initialization fails, which is a system-level issue. Using expect()
        // here is acceptable -- there's no reasonable recovery path.
        let client = reqwest::Client::builder()
            .timeout(timeout.unwrap_or(Duration::from_secs(5)))
            .build()
            .expect("TLS backend initialization failed -- cannot create HTTP client");

        Self {
            endpoint,
            api_key,
            client,
        }
    }

    /// Retry a BAML request with exponential backoff.
    ///
    /// Matches the Python reference implementation's `_retry_baml_request()`.
    /// Retries up to MAX_RETRIES times with exponential backoff starting at
    /// INITIAL_DELAY_MS and capped at MAX_DELAY_MS.
    pub(crate) async fn retry_request<F, Fut, T>(&self, request_fn: F) -> Result<T>
    where
        F: Fn() -> Fut,
        Fut: std::future::Future<Output = Result<T>>,
    {
        let mut delay_ms = INITIAL_DELAY_MS;
        let mut last_error = None;

        for attempt in 0..=MAX_RETRIES {
            match request_fn().await {
                Ok(result) => return Ok(result),
                Err(e) => {
                    if attempt < MAX_RETRIES {
                        warn!(
                            "BAML request failed (attempt {}/{}): {}, retrying in {}ms",
                            attempt + 1,
                            MAX_RETRIES + 1,
                            e,
                            delay_ms
                        );
                        tokio::time::sleep(Duration::from_millis(delay_ms)).await;
                        delay_ms = ((delay_ms as f64) * BACKOFF_MULTIPLIER).min(MAX_DELAY_MS as f64)
                            as u64;
                    }
                    last_error = Some(e);
                }
            }
        }

        Err(last_error.expect("retry loop must execute at least once"))
    }

    /// Internal: single attempt at AnalyzeCliText
    async fn analyze_cli_text_once(
        &self,
        cli_lines: &[String],
        previous_protocol: &str,
        previous_commands: &[String],
    ) -> Result<KeystrokeAnalysisResponse> {
        let function_endpoint = format!("{}/AnalyzeCliText", self.endpoint.trim_end_matches('/'));

        let request = AnalyzeCliTextRequest {
            cli_lines: cli_lines.to_vec(),
            previous_protocol: previous_protocol.to_string(),
            previous_commands: previous_commands.to_vec(),
        };

        let mut req = self.client.post(&function_endpoint).json(&request);

        if let Some(ref key) = self.api_key {
            req = req.header("Authorization", format!("Bearer {}", key));
        }

        req = req.header("Content-Type", "application/json");

        let response = req.send().await.map_err(ThreatDetectionError::HttpError)?;

        if !response.status().is_success() {
            let status = response.status();
            let error_text = response
                .text()
                .await
                .unwrap_or_else(|_| "Unknown error".to_string());
            error!("BAML AnalyzeCliText API error: {} - {}", status, error_text);
            return Err(ThreatDetectionError::BamlApiError(format!(
                "HTTP {}: {}",
                status, error_text
            )));
        }

        let baml_response: KeystrokeAnalysisResponse = response
            .json()
            .await
            .map_err(ThreatDetectionError::HttpError)?;

        Ok(baml_response)
    }

    /// Analyze CLI text with richer context using BAML AnalyzeCliText function
    ///
    /// This is the richer analysis endpoint that accepts protocol context and
    /// previous command history, matching the Python reference implementation.
    /// Retries with exponential backoff on transient failures.
    ///
    /// # Arguments
    ///
    /// * `cli_lines` - Lines of CLI text to analyze
    /// * `previous_protocol` - The protocol being used (e.g., "ssh", "rdp")
    /// * `previous_commands` - Previous commands for context
    ///
    /// # Returns
    ///
    /// KeystrokeAnalysisResponse with analysis_report and overall_summary
    pub async fn analyze_cli_text(
        &self,
        cli_lines: &[String],
        previous_protocol: &str,
        previous_commands: &[String],
    ) -> Result<KeystrokeAnalysisResponse> {
        debug!(
            "BAML: Analyzing CLI text ({} lines, protocol: {}, {} previous commands)",
            cli_lines.len(),
            previous_protocol,
            previous_commands.len()
        );

        let lines = cli_lines.to_vec();
        let protocol = previous_protocol.to_string();
        let prev_cmds = previous_commands.to_vec();
        let result = self
            .retry_request(|| {
                let lines_ref = lines.as_slice();
                let protocol_ref = protocol.as_str();
                let prev_cmds_ref = prev_cmds.as_slice();
                async move {
                    self.analyze_cli_text_once(lines_ref, protocol_ref, prev_cmds_ref)
                        .await
                }
            })
            .await?;

        debug!(
            "BAML: AnalyzeCliText complete - {} reports, summary: {}",
            result.analysis_report.len(),
            result.overall_summary
        );

        Ok(result)
    }

    /// Internal: single attempt at ExtractCommandSummary
    async fn extract_command_summary_once(
        &self,
        command_sequence: &[String],
    ) -> Result<CommandSummaryResponse> {
        let function_endpoint = format!(
            "{}/ExtractCommandSummary",
            self.endpoint.trim_end_matches('/')
        );

        let request = ExtractCommandSummaryRequest {
            command_sequence: command_sequence.to_vec(),
        };

        let mut req = self.client.post(&function_endpoint).json(&request);

        if let Some(ref key) = self.api_key {
            req = req.header("Authorization", format!("Bearer {}", key));
        }

        req = req.header("Content-Type", "application/json");

        let response = req.send().await.map_err(ThreatDetectionError::HttpError)?;

        if !response.status().is_success() {
            let status = response.status();
            let error_text = response
                .text()
                .await
                .unwrap_or_else(|_| "Unknown error".to_string());
            error!("BAML API error: {} - {}", status, error_text);
            return Err(ThreatDetectionError::BamlApiError(format!(
                "HTTP {}: {}",
                status, error_text
            )));
        }

        let baml_response: CommandSummaryResponse = response
            .json()
            .await
            .map_err(ThreatDetectionError::HttpError)?;

        Ok(baml_response)
    }

    /// Generate command summary using BAML ExtractCommandSummary function
    ///
    /// Retries with exponential backoff on transient failures.
    ///
    /// # Arguments
    ///
    /// * `command_sequence` - List of commands in order
    ///
    /// # Returns
    ///
    /// CommandSummaryResponse with overall_summary and optional risk fields
    pub async fn extract_command_summary(
        &self,
        command_sequence: &[String],
    ) -> Result<CommandSummaryResponse> {
        debug!(
            "BAML: Generating summary for {} commands",
            command_sequence.len()
        );

        let cmds = command_sequence.to_vec();
        let result = self
            .retry_request(|| {
                let cmds_ref = cmds.as_slice();
                async move { self.extract_command_summary_once(cmds_ref).await }
            })
            .await?;

        debug!("BAML: Summary generated: {}", result.overall_summary);

        Ok(result)
    }

    /// Convert BAML Analysis to ThreatResult
    ///
    /// Maps categorical risk_level and optional numeric risk_score from BAML
    /// response into a ThreatResult. Uses numeric score from LLM if provided,
    /// otherwise derives from categorical level.
    pub fn analysis_to_threat_result(
        &self,
        analysis: &Analysis,
        overall_summary: &str,
    ) -> ThreatResult {
        let risk_level_lower = analysis.risk_level.to_lowercase();

        let level = match risk_level_lower.as_str() {
            "critical" => ThreatLevel::Critical,
            "high" => ThreatLevel::High,
            "medium" => ThreatLevel::Medium,
            "low" => ThreatLevel::Low,
            _ => ThreatLevel::None,
        };

        // Use numeric score from LLM if provided, otherwise derive from categorical level
        let risk_score = analysis.risk_score.unwrap_or_else(|| level.to_risk_score());

        ThreatResult {
            level,
            risk_score,
            risk_level_source: RiskSource::ModelDefault,
            confidence: 0.8,
            description: format!("{} - {}", analysis.risk_category, analysis.reasoning),
            action: if level == ThreatLevel::Critical || level == ThreatLevel::High {
                "terminate".to_string()
            } else {
                "monitor".to_string()
            },
            command_text: analysis.command_text.clone(),
            risk_category: Some(analysis.risk_category.clone()),
            tag_matches: TagMatches::default(),
            should_terminate_session: matches!(level, ThreatLevel::Critical | ThreatLevel::High),
            metadata: serde_json::json!({
                "risk_category": analysis.risk_category,
                "reasoning": analysis.reasoning,
                "overall_summary": overall_summary,
                "action_effects": analysis.action_effects,
            }),
        }
    }

    /// Internal: single attempt at AnalyzeScreenshot
    async fn analyze_screenshot_once(
        &self,
        image_b64: &str,
        buffered_keystrokes: &str,
        session_id: &str,
    ) -> Result<KeystrokeAnalysisResponse> {
        let function_endpoint =
            format!("{}/AnalyzeScreenshot", self.endpoint.trim_end_matches('/'));

        let request = AnalyzeScreenshotRequest {
            image_b64: image_b64.to_string(),
            buffered_keystrokes: buffered_keystrokes.to_string(),
            session_id: session_id.to_string(),
        };

        let mut req = self.client.post(&function_endpoint).json(&request);

        if let Some(ref key) = self.api_key {
            req = req.header("Authorization", format!("Bearer {}", key));
        }

        req = req.header("Content-Type", "application/json");

        let response = req.send().await.map_err(ThreatDetectionError::HttpError)?;

        if !response.status().is_success() {
            let status = response.status();
            let error_text = response
                .text()
                .await
                .unwrap_or_else(|_| "Unknown error".to_string());
            error!(
                "BAML AnalyzeScreenshot API error: {} - {}",
                status, error_text
            );
            return Err(ThreatDetectionError::BamlApiError(format!(
                "HTTP {}: {}",
                status, error_text
            )));
        }

        let baml_response: KeystrokeAnalysisResponse = response
            .json()
            .await
            .map_err(ThreatDetectionError::HttpError)?;

        Ok(baml_response)
    }

    /// Analyze a grayscale JPEG screenshot using BAML AnalyzeScreenshot.
    ///
    /// Retries with exponential backoff on transient failures.
    ///
    /// # Arguments
    ///
    /// * `image_b64` — Base64-encoded grayscale JPEG bytes.
    /// * `buffered_keystrokes` — Keystrokes accumulated since last trigger.
    /// * `session_id` — Session identifier for logging context.
    ///
    /// # Returns
    ///
    /// `KeystrokeAnalysisResponse` with analysis reports and overall summary.
    pub async fn analyze_screenshot(
        &self,
        image_b64: &str,
        buffered_keystrokes: &str,
        session_id: &str,
    ) -> Result<KeystrokeAnalysisResponse> {
        debug!(
            "BAML: Analyzing screenshot ({} b64 bytes, {} keystroke bytes, session={})",
            image_b64.len(),
            buffered_keystrokes.len(),
            session_id
        );

        let b64 = image_b64.to_string();
        let keystrokes = buffered_keystrokes.to_string();
        let sid = session_id.to_string();
        let result = self
            .retry_request(|| {
                let b64_ref = b64.as_str();
                let ks_ref = keystrokes.as_str();
                let sid_ref = sid.as_str();
                async move { self.analyze_screenshot_once(b64_ref, ks_ref, sid_ref).await }
            })
            .await?;

        debug!(
            "BAML: AnalyzeScreenshot complete - {} reports",
            result.analysis_report.len()
        );

        Ok(result)
    }

    /// Health check - test BAML API connectivity
    pub async fn health_check(&self) -> Result<()> {
        let test_lines = vec!["ls".to_string()];
        match self.analyze_cli_text(&test_lines, "ssh", &[]).await {
            Ok(_) => Ok(()),
            Err(e) => {
                warn!("BAML health check failed: {}", e);
                Err(e)
            }
        }
    }
}
