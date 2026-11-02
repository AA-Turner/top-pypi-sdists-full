use crate::chat_completions_openai::types::*;
use crate::convert::ctx::ConversionCtx;
use crate::error::WarningAction;
use crate::open_responses::types::*;

pub(crate) fn warn_dropped_chat_completions_usage_details(
    usage: &ChatCompletionsUsage,
    ctx: &mut ConversionCtx<()>,
    field_prefix: &str,
) {
    if let Some(details) = &usage.prompt_tokens_details {
        warn_dropped_usage_detail(
            &details.audio_tokens,
            &format!("{field_prefix}.prompt_tokens_details.audio_tokens"),
            ctx,
        );
    }

    if let Some(details) = &usage.completion_tokens_details {
        warn_dropped_usage_detail(
            &details.audio_tokens,
            &format!("{field_prefix}.completion_tokens_details.audio_tokens"),
            ctx,
        );
        warn_dropped_usage_detail(
            &details.accepted_prediction_tokens,
            &format!("{field_prefix}.completion_tokens_details.accepted_prediction_tokens"),
            ctx,
        );
        warn_dropped_usage_detail(
            &details.rejected_prediction_tokens,
            &format!("{field_prefix}.completion_tokens_details.rejected_prediction_tokens"),
            ctx,
        );
    }
}

fn warn_dropped_usage_detail(value: &Option<u64>, field: &str, ctx: &mut ConversionCtx<()>) {
    if value.is_some_and(|tokens| tokens > 0) {
        ctx.warn(
            field,
            WarningAction::Dropped,
            "not supported in Open Responses usage",
        );
    }
}

impl From<ChatCompletionsUsage> for Usage {
    fn from(value: ChatCompletionsUsage) -> Self {
        Self {
            input_tokens: value.prompt_tokens,
            output_tokens: value.completion_tokens,
            total_tokens: value.total_tokens,
            input_tokens_details: Some(InputTokensDetails {
                cached_tokens: value
                    .prompt_tokens_details
                    .as_ref()
                    .and_then(|details| details.cached_tokens)
                    .unwrap_or(0),
                cache_write_tokens: value
                    .prompt_tokens_details
                    .and_then(|details| details.cache_write_tokens)
                    .filter(|tokens| *tokens > 0),
            }),
            output_tokens_details: Some(OutputTokensDetails {
                reasoning_tokens: value
                    .completion_tokens_details
                    .and_then(|details| details.reasoning_tokens)
                    .unwrap_or(0),
            }),
        }
    }
}

impl From<Usage> for ChatCompletionsUsage {
    fn from(value: Usage) -> Self {
        Self {
            prompt_tokens: value.input_tokens,
            completion_tokens: value.output_tokens,
            total_tokens: value.total_tokens,
            prompt_tokens_details: value.input_tokens_details.map(|details| {
                ChatCompletionsPromptTokensDetails {
                    cached_tokens: Some(details.cached_tokens),
                    cache_write_tokens: details.cache_write_tokens,
                    audio_tokens: Some(0),
                }
            }),
            completion_tokens_details: value.output_tokens_details.map(|details| {
                ChatCompletionsCompletionTokensDetails {
                    reasoning_tokens: Some(details.reasoning_tokens),
                    audio_tokens: Some(0),
                    accepted_prediction_tokens: None,
                    rejected_prediction_tokens: None,
                }
            }),
        }
    }
}

pub(crate) fn chat_completions_finish_reason_to_open_responses_status(
    finish_reason: Option<ChatCompletionsFinishReason>,
) -> (ResponseStatus, Option<IncompleteDetails>) {
    match finish_reason {
        None
        | Some(ChatCompletionsFinishReason::Stop)
        | Some(ChatCompletionsFinishReason::ToolCalls) => (ResponseStatus::Completed, None),
        Some(ChatCompletionsFinishReason::Length) => (
            ResponseStatus::Incomplete,
            Some(IncompleteDetails {
                reason: "max_output_tokens".into(),
            }),
        ),
        Some(ChatCompletionsFinishReason::ContentFilter)
        | Some(ChatCompletionsFinishReason::Error) => (ResponseStatus::Failed, None),
    }
}

pub(crate) fn open_responses_status_to_chat_completions_finish_reason(
    status: ResponseStatus,
    output: &[OutputItem],
) -> Option<ChatCompletionsFinishReason> {
    match status {
        ResponseStatus::Completed => {
            let has_function_call = output.iter().any(|item| {
                matches!(
                    item,
                    OutputItem::FunctionCall { .. } | OutputItem::CustomToolCall { .. }
                )
            });
            if has_function_call {
                Some(ChatCompletionsFinishReason::ToolCalls)
            } else {
                Some(ChatCompletionsFinishReason::Stop)
            }
        }
        ResponseStatus::Incomplete => Some(ChatCompletionsFinishReason::Length),
        ResponseStatus::Failed => Some(ChatCompletionsFinishReason::Error),
        ResponseStatus::InProgress | ResponseStatus::Queued => None,
    }
}
