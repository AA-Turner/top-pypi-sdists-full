use crate::error::ConversionError;
use crate::open_responses::types::ReasoningEffort;

pub struct AnthropicConvertConfig {
    pub default_max_tokens: u64,
    /// Maps reasoning effort levels to fractions of max_tokens.
    ///
    /// Used by **AM → OR** (`budget_to_effort`): computes
    /// `ratio = budget_tokens / max_tokens`, then finds the first entry whose
    /// fraction is `>= ratio`.
    ///
    /// Entries must be sorted by fraction ascending.
    pub reasoning_fractions: &'static [(ReasoningEffort, f64)],
    pub strip_encrypted_reasoning: bool,
    /// The Anthropic web search server tool type used when converting OR→AM.
    pub web_search_type: &'static str,
    /// The Anthropic web search server tool name used when converting OR→AM.
    pub web_search_name: &'static str,
    /// The Anthropic tool search server tool type used when converting OR→AM.
    pub tool_search_type: &'static str,
    /// The Anthropic tool search server tool name used when converting OR→AM.
    pub tool_search_name: &'static str,
}

impl Default for AnthropicConvertConfig {
    fn default() -> Self {
        Self {
            default_max_tokens: 32_000,
            reasoning_fractions: &[
                (ReasoningEffort::Minimal, 0.05),
                (ReasoningEffort::Low, 0.10),
                (ReasoningEffort::Medium, 0.25),
                (ReasoningEffort::High, 0.50),
                (ReasoningEffort::Xhigh, 0.80),
            ],
            strip_encrypted_reasoning: false,
            web_search_type: "web_search_20260209",
            web_search_name: "web_search",
            tool_search_type: "tool_search_tool_bm25_20251119",
            tool_search_name: "tool_search_tool_bm25",
        }
    }
}

impl AnthropicConvertConfig {
    /// Maps `budget_tokens / max_tokens` ratio to a reasoning effort level.
    ///
    /// Computes `ratio = budget_tokens / max_tokens` and finds the first entry
    /// in `reasoning_fractions` whose fraction is `>= ratio`. Values beyond the
    /// highest fraction map to the last effort level.
    ///
    /// Returns `ConversionError` if `max_tokens` is less than 2.
    pub fn budget_to_effort(
        &self,
        budget_tokens: u64,
        max_tokens: u64,
    ) -> Result<ReasoningEffort, ConversionError> {
        if max_tokens < 2 {
            return Err(ConversionError::InvalidInput(format!(
                "max_tokens must be at least 2 for reasoning, got {max_tokens}"
            )));
        }
        let ratio = budget_tokens as f64 / max_tokens as f64;
        let effort = self
            .reasoning_fractions
            .iter()
            .find(|(_, f)| ratio <= *f)
            .map(|(e, _)| e.clone())
            .unwrap_or_else(|| {
                self.reasoning_fractions
                    .last()
                    .map(|(e, _)| e.clone())
                    .unwrap_or(ReasoningEffort::Xhigh)
            });
        Ok(effort)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    // ── budget_to_effort ──

    #[test]
    fn budget_to_effort_ratio_based() {
        let config = AnthropicConvertConfig::default();
        let max = 10_000u64;
        // 0% → Minimal
        assert_eq!(
            config.budget_to_effort(0, max).unwrap(),
            ReasoningEffort::Minimal
        );
        // 5% boundary → Minimal
        assert_eq!(
            config.budget_to_effort(500, max).unwrap(),
            ReasoningEffort::Minimal
        );
        // 6% → Low
        assert_eq!(
            config.budget_to_effort(600, max).unwrap(),
            ReasoningEffort::Low
        );
        // 10% boundary → Low
        assert_eq!(
            config.budget_to_effort(1000, max).unwrap(),
            ReasoningEffort::Low
        );
        // 11% → Medium
        assert_eq!(
            config.budget_to_effort(1100, max).unwrap(),
            ReasoningEffort::Medium
        );
        // 25% boundary → Medium
        assert_eq!(
            config.budget_to_effort(2500, max).unwrap(),
            ReasoningEffort::Medium
        );
        // 26% → High
        assert_eq!(
            config.budget_to_effort(2600, max).unwrap(),
            ReasoningEffort::High
        );
        // 50% boundary → High
        assert_eq!(
            config.budget_to_effort(5000, max).unwrap(),
            ReasoningEffort::High
        );
        // 51% → Xhigh
        assert_eq!(
            config.budget_to_effort(5100, max).unwrap(),
            ReasoningEffort::Xhigh
        );
        // 80% boundary → Xhigh
        assert_eq!(
            config.budget_to_effort(8000, max).unwrap(),
            ReasoningEffort::Xhigh
        );
        // 99% → Xhigh
        assert_eq!(
            config.budget_to_effort(9900, max).unwrap(),
            ReasoningEffort::Xhigh
        );
    }

    #[test]
    fn budget_to_effort_small_max_tokens() {
        let config = AnthropicConvertConfig::default();
        // max_tokens=2, budget=1 → 50% → High
        assert_eq!(
            config.budget_to_effort(1, 2).unwrap(),
            ReasoningEffort::High
        );
        // max_tokens=100, budget=3 → 3% → Minimal
        assert_eq!(
            config.budget_to_effort(3, 100).unwrap(),
            ReasoningEffort::Minimal
        );
    }

    #[test]
    fn budget_to_effort_max_tokens_below_2_errors() {
        let config = AnthropicConvertConfig::default();
        assert!(config.budget_to_effort(100, 0).is_err());
        assert!(config.budget_to_effort(1, 1).is_err());
    }

    #[test]
    fn budget_to_effort_budget_exceeds_max_is_xhigh() {
        let config = AnthropicConvertConfig::default();
        // Invalid input (budget > max), but should not panic — ratio > 1.0 → Xhigh
        assert_eq!(
            config.budget_to_effort(2000, 1000).unwrap(),
            ReasoningEffort::Xhigh
        );
    }
}
