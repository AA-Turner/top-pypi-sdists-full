use crate::chat_completions_openai::types::*;
use crate::convert::ctx::ConversionCtx;
use crate::convert::mapping::LossyTryFromWithCtx;
use crate::error::WarningAction;
use crate::open_responses::types::{ImageDetail, ReasoningEffort, ServiceTier, Verbosity};

impl LossyTryFromWithCtx<ChatCompletionsImageDetail> for ImageDetail {
    fn lossy_try_from(
        value: ChatCompletionsImageDetail,
        ctx: &mut ConversionCtx<()>,
        field: &str,
    ) -> Option<Self> {
        match value {
            ChatCompletionsImageDetail::Known(ChatCompletionsKnownImageDetail::Auto) => {
                Some(ImageDetail::Auto)
            }
            ChatCompletionsImageDetail::Known(ChatCompletionsKnownImageDetail::Low) => {
                Some(ImageDetail::Low)
            }
            ChatCompletionsImageDetail::Known(ChatCompletionsKnownImageDetail::High) => {
                Some(ImageDetail::High)
            }
            ChatCompletionsImageDetail::Other(value) => {
                ctx.warn(
                    field,
                    WarningAction::Dropped,
                    format!("unknown image detail '{value}'"),
                );
                None
            }
        }
    }
}

impl From<ImageDetail> for ChatCompletionsImageDetail {
    fn from(value: ImageDetail) -> Self {
        match value {
            ImageDetail::Auto => {
                ChatCompletionsImageDetail::Known(ChatCompletionsKnownImageDetail::Auto)
            }
            ImageDetail::Low => {
                ChatCompletionsImageDetail::Known(ChatCompletionsKnownImageDetail::Low)
            }
            ImageDetail::High => {
                ChatCompletionsImageDetail::Known(ChatCompletionsKnownImageDetail::High)
            }
        }
    }
}

impl From<ChatCompletionsVerbosity> for Verbosity {
    fn from(value: ChatCompletionsVerbosity) -> Self {
        match value {
            ChatCompletionsVerbosity::Low => Verbosity::Low,
            ChatCompletionsVerbosity::Medium => Verbosity::Medium,
            ChatCompletionsVerbosity::High => Verbosity::High,
        }
    }
}

impl From<Verbosity> for ChatCompletionsVerbosity {
    fn from(value: Verbosity) -> Self {
        match value {
            Verbosity::Low => ChatCompletionsVerbosity::Low,
            Verbosity::Medium => ChatCompletionsVerbosity::Medium,
            Verbosity::High => ChatCompletionsVerbosity::High,
        }
    }
}

impl From<ServiceTier> for ChatCompletionsServiceTier {
    fn from(value: ServiceTier) -> Self {
        match value {
            ServiceTier::Auto => {
                ChatCompletionsServiceTier::Known(ChatCompletionsKnownServiceTier::Auto)
            }
            ServiceTier::Default => {
                ChatCompletionsServiceTier::Known(ChatCompletionsKnownServiceTier::Default)
            }
            ServiceTier::Flex => {
                ChatCompletionsServiceTier::Known(ChatCompletionsKnownServiceTier::Flex)
            }
            ServiceTier::Priority => {
                ChatCompletionsServiceTier::Known(ChatCompletionsKnownServiceTier::Priority)
            }
        }
    }
}

impl LossyTryFromWithCtx<ChatCompletionsReasoningEffort> for ReasoningEffort {
    fn lossy_try_from(
        value: ChatCompletionsReasoningEffort,
        _ctx: &mut ConversionCtx<()>,
        _field: &str,
    ) -> Option<Self> {
        Some(match value {
            ChatCompletionsReasoningEffort::None => ReasoningEffort::None,
            ChatCompletionsReasoningEffort::Minimal => ReasoningEffort::Minimal,
            ChatCompletionsReasoningEffort::Low => ReasoningEffort::Low,
            ChatCompletionsReasoningEffort::Medium => ReasoningEffort::Medium,
            ChatCompletionsReasoningEffort::High => ReasoningEffort::High,
            ChatCompletionsReasoningEffort::Xhigh => ReasoningEffort::Xhigh,
            ChatCompletionsReasoningEffort::Max => ReasoningEffort::Max,
        })
    }
}

impl LossyTryFromWithCtx<ChatCompletionsServiceTier> for ServiceTier {
    fn lossy_try_from(
        value: ChatCompletionsServiceTier,
        ctx: &mut ConversionCtx<()>,
        field: &str,
    ) -> Option<Self> {
        Some(match value {
            ChatCompletionsServiceTier::Known(ChatCompletionsKnownServiceTier::Auto) => {
                ServiceTier::Auto
            }
            ChatCompletionsServiceTier::Known(ChatCompletionsKnownServiceTier::Default) => {
                ServiceTier::Default
            }
            ChatCompletionsServiceTier::Known(ChatCompletionsKnownServiceTier::Flex) => {
                ServiceTier::Flex
            }
            ChatCompletionsServiceTier::Known(ChatCompletionsKnownServiceTier::Priority) => {
                ServiceTier::Priority
            }
            ChatCompletionsServiceTier::Known(ChatCompletionsKnownServiceTier::Scale) => {
                ctx.warn(
                    field,
                    WarningAction::Changed,
                    "service_tier=scale is not available in Open Responses and was mapped to priority",
                );
                ServiceTier::Priority
            }
            ChatCompletionsServiceTier::Other(value) => {
                ctx.warn(
                    field,
                    WarningAction::Dropped,
                    format!("unknown service_tier '{value}'"),
                );
                return None;
            }
        })
    }
}
