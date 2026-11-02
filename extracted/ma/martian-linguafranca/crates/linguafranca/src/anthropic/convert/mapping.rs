use crate::anthropic::convert::config::AnthropicConvertConfig;
use crate::anthropic::types::{
    AnthropicKnownServiceTier, AnthropicOutputEffort, AnthropicServiceTier,
};
use crate::convert::ctx::ConversionCtx;
use crate::convert::mapping::LossyTryFromWithCtx;
use crate::error::WarningAction;
use crate::open_responses::types::{ReasoningEffort, ServiceTier};

// ── AnthropicOutputEffort ↔ ReasoningEffort ──

impl LossyTryFromWithCtx<AnthropicOutputEffort, AnthropicConvertConfig> for ReasoningEffort {
    fn lossy_try_from(
        value: AnthropicOutputEffort,
        _ctx: &mut ConversionCtx<AnthropicConvertConfig>,
        _field: &str,
    ) -> Option<Self> {
        Some(match value {
            AnthropicOutputEffort::Low => ReasoningEffort::Low,
            AnthropicOutputEffort::Medium => ReasoningEffort::Medium,
            AnthropicOutputEffort::High => ReasoningEffort::High,
            AnthropicOutputEffort::Xhigh => ReasoningEffort::Xhigh,
            AnthropicOutputEffort::Max => ReasoningEffort::Max,
        })
    }
}

impl LossyTryFromWithCtx<ReasoningEffort, AnthropicConvertConfig> for AnthropicOutputEffort {
    fn lossy_try_from(
        value: ReasoningEffort,
        ctx: &mut ConversionCtx<AnthropicConvertConfig>,
        field: &str,
    ) -> Option<Self> {
        match value {
            ReasoningEffort::None => None,
            ReasoningEffort::Minimal => {
                ctx.warn(
                    field,
                    WarningAction::Changed,
                    "minimal effort not supported in Anthropic output_config; mapped to low",
                );
                Some(AnthropicOutputEffort::Low)
            }
            ReasoningEffort::Low => Some(AnthropicOutputEffort::Low),
            ReasoningEffort::Medium => Some(AnthropicOutputEffort::Medium),
            ReasoningEffort::High => Some(AnthropicOutputEffort::High),
            ReasoningEffort::Xhigh => Some(AnthropicOutputEffort::Xhigh),
            ReasoningEffort::Max => Some(AnthropicOutputEffort::Max),
        }
    }
}

impl From<AnthropicKnownServiceTier> for ServiceTier {
    fn from(value: AnthropicKnownServiceTier) -> Self {
        match value {
            AnthropicKnownServiceTier::Auto => ServiceTier::Auto,
            AnthropicKnownServiceTier::Standard => ServiceTier::Default,
            AnthropicKnownServiceTier::Priority => ServiceTier::Priority,
        }
    }
}

impl LossyTryFromWithCtx<AnthropicServiceTier, AnthropicConvertConfig> for ServiceTier {
    fn lossy_try_from(
        value: AnthropicServiceTier,
        ctx: &mut ConversionCtx<AnthropicConvertConfig>,
        field: &str,
    ) -> Option<Self> {
        match value {
            AnthropicServiceTier::Known(known) => Some(known.into()),
            AnthropicServiceTier::Other(value) => match value.as_str() {
                // Backward compatibility for older fixtures/inputs.
                "default" => Some(ServiceTier::Default),
                "flex" => Some(ServiceTier::Flex),
                other => {
                    ctx.warn(
                        field,
                        WarningAction::Dropped,
                        format!("unknown Anthropic service_tier '{other}'"),
                    );
                    None
                }
            },
        }
    }
}

impl LossyTryFromWithCtx<ServiceTier, AnthropicConvertConfig> for AnthropicServiceTier {
    fn lossy_try_from(
        value: ServiceTier,
        ctx: &mut ConversionCtx<AnthropicConvertConfig>,
        field: &str,
    ) -> Option<Self> {
        Some(match value {
            ServiceTier::Auto => AnthropicServiceTier::Known(AnthropicKnownServiceTier::Auto),
            ServiceTier::Default => {
                AnthropicServiceTier::Known(AnthropicKnownServiceTier::Standard)
            }
            ServiceTier::Priority => {
                AnthropicServiceTier::Known(AnthropicKnownServiceTier::Priority)
            }
            ServiceTier::Flex => {
                ctx.warn(
                    field,
                    WarningAction::Changed,
                    "service_tier=flex is not available in Anthropic and was mapped to standard",
                );
                AnthropicServiceTier::Known(AnthropicKnownServiceTier::Standard)
            }
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::anthropic::convert::ctx::ConversionCtx as AnthropicConversionCtx;

    // ── output effort mapping tests ──

    #[test]
    fn am_low_effort_maps_to_or_low() {
        let mut ctx = AnthropicConversionCtx::new();
        let effort = ReasoningEffort::lossy_try_from(
            AnthropicOutputEffort::Low,
            &mut ctx,
            "output_config.effort",
        );
        assert_eq!(effort, Some(ReasoningEffort::Low));
        assert!(ctx.into_warnings().is_empty());
    }

    #[test]
    fn am_xhigh_effort_maps_to_or_xhigh() {
        let mut ctx = AnthropicConversionCtx::new();
        let effort = ReasoningEffort::lossy_try_from(
            AnthropicOutputEffort::Xhigh,
            &mut ctx,
            "output_config.effort",
        );
        assert_eq!(effort, Some(ReasoningEffort::Xhigh));
        assert!(ctx.into_warnings().is_empty());
    }

    #[test]
    fn am_max_effort_maps_to_or_max() {
        let mut ctx = AnthropicConversionCtx::new();
        let effort = ReasoningEffort::lossy_try_from(
            AnthropicOutputEffort::Max,
            &mut ctx,
            "output_config.effort",
        );
        assert_eq!(effort, Some(ReasoningEffort::Max));
        assert!(ctx.into_warnings().is_empty());
    }

    #[test]
    fn or_none_effort_maps_to_no_am_effort() {
        let mut ctx = AnthropicConversionCtx::new();
        let effort = AnthropicOutputEffort::lossy_try_from(
            ReasoningEffort::None,
            &mut ctx,
            "output_config.effort",
        );
        assert_eq!(effort, None);
        assert!(ctx.into_warnings().is_empty());
    }

    #[test]
    fn or_minimal_effort_maps_to_am_low_with_warning() {
        let mut ctx = AnthropicConversionCtx::new();
        let effort = AnthropicOutputEffort::lossy_try_from(
            ReasoningEffort::Minimal,
            &mut ctx,
            "output_config.effort",
        );
        assert_eq!(effort, Some(AnthropicOutputEffort::Low));
        let warnings = ctx.into_warnings();
        assert_eq!(warnings.len(), 1);
        assert!(warnings[0].message.contains("minimal"));
    }

    #[test]
    fn or_xhigh_effort_maps_to_am_xhigh() {
        let mut ctx = AnthropicConversionCtx::new();
        let effort = AnthropicOutputEffort::lossy_try_from(
            ReasoningEffort::Xhigh,
            &mut ctx,
            "output_config.effort",
        );
        assert_eq!(effort, Some(AnthropicOutputEffort::Xhigh));
        assert!(ctx.into_warnings().is_empty());
    }

    #[test]
    fn or_max_effort_maps_to_am_max() {
        let mut ctx = AnthropicConversionCtx::new();
        let effort = AnthropicOutputEffort::lossy_try_from(
            ReasoningEffort::Max,
            &mut ctx,
            "output_config.effort",
        );
        assert_eq!(effort, Some(AnthropicOutputEffort::Max));
        assert!(ctx.into_warnings().is_empty());
    }

    // ── service tier mapping tests ──

    #[test]
    fn known_service_tier_maps_to_open_responses() {
        let mut ctx = AnthropicConversionCtx::new();
        let tier = ServiceTier::lossy_try_from(
            AnthropicServiceTier::Known(AnthropicKnownServiceTier::Standard),
            &mut ctx,
            "service_tier",
        );
        assert_eq!(tier, Some(ServiceTier::Default));
        assert!(ctx.into_warnings().is_empty());
    }

    #[test]
    fn legacy_default_string_maps_to_default_without_warning() {
        let mut ctx = AnthropicConversionCtx::new();
        let tier = ServiceTier::lossy_try_from(
            AnthropicServiceTier::Other("default".into()),
            &mut ctx,
            "service_tier",
        );
        assert_eq!(tier, Some(ServiceTier::Default));
        assert!(ctx.into_warnings().is_empty());
    }

    #[test]
    fn unknown_anthropic_service_tier_warns_and_drops() {
        let mut ctx = AnthropicConversionCtx::new();
        let tier = ServiceTier::lossy_try_from(
            AnthropicServiceTier::Other("burst".into()),
            &mut ctx,
            "service_tier",
        );
        assert_eq!(tier, None);
        let warnings = ctx.into_warnings();
        assert_eq!(warnings.len(), 1);
        assert_eq!(warnings[0].field, "service_tier");
    }

    #[test]
    fn flex_maps_to_standard_with_warning() {
        let mut ctx = AnthropicConversionCtx::new();
        let tier =
            AnthropicServiceTier::lossy_try_from(ServiceTier::Flex, &mut ctx, "service_tier");
        assert_eq!(
            tier,
            Some(AnthropicServiceTier::Known(
                AnthropicKnownServiceTier::Standard
            ))
        );
        let warnings = ctx.into_warnings();
        assert_eq!(warnings.len(), 1);
        assert_eq!(warnings[0].field, "service_tier");
    }
}
