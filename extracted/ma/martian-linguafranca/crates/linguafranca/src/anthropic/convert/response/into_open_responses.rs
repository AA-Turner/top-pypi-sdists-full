// ID strategy: regular Open Responses output items synthesized by this
// converter (messages, reasoning, function calls) get opaque deterministic OR
// item IDs. Search/tool-search items intentionally preserve or derive from
// Anthropic tool-use IDs because those IDs are required to correlate server
// tool calls with their result blocks during OR↔AM round trips.

use crate::anthropic::convert::ctx::ConversionCtx;
use crate::anthropic::convert::helpers::*;
use crate::anthropic::response::AnthropicResponse;
use crate::anthropic::types::*;
use crate::config::ConversionConfig;
use crate::convert::mapping::LossyTryFromWithCtx;
use crate::convert::open_responses_id::OpenResponsesOutputItemKind;
use crate::convert::open_responses_output_accum::OpenResponsesOutputAccum;
use crate::convert::tool_namespace::{split_tool_name, tool_references_from_flat_names};
use crate::error::{ConversionError, ConversionResult, WarningAction};
use crate::open_responses::response::OpenResponsesResponse;
use crate::open_responses::types::*;
use crate::traits::IntoOpenResponses;

impl IntoOpenResponses for AnthropicResponse {
    type Target = OpenResponsesResponse;

    fn into_open_responses(
        self,
        _config: Option<ConversionConfig>,
    ) -> Result<ConversionResult<OpenResponsesResponse>, ConversionError> {
        let mut ctx = ConversionCtx::new();
        let mut accum = OpenResponsesOutputAccum::new(self.id.clone());

        convert_content_blocks(&mut accum, self.content, &mut ctx);

        let (status, incomplete_details) =
            convert_anthropic_messages_stop_reason_to_open_responses(self.stop_reason);

        let mut result = ConversionResult::with_warnings(
            OpenResponsesResponse {
                id: self.id,
                object: "response".into(),
                created_at: 0,
                status,
                model: self.model,
                output: accum.into_items(),
                incomplete_details,
                service_tier: self
                    .service_tier
                    .or(self.usage.service_tier.clone())
                    .and_then(|tier| ServiceTier::lossy_try_from(tier, &mut ctx, "service_tier")),
                usage: Some(self.usage.into()),
                ..Default::default()
            },
            ctx.into_warnings(),
        );

        result.warn_unsupported(
            "Open Responses",
            &[
                ("container", self.container.is_some()),
                ("stop_sequence", self.stop_sequence.is_some()),
            ],
        );

        Ok(result)
    }
}

fn convert_content_blocks(
    accum: &mut OpenResponsesOutputAccum,
    blocks: Vec<AnthropicOutputContentBlock>,
    ctx: &mut ConversionCtx,
) {
    // server_tool_use always precedes its matching web_search_tool_result
    let mut pending_web_search: Option<(String, Option<String>)> = None; // (id, query)
    let mut pending_tool_search: Option<(String, serde_json::Value)> = None; // (id, input)

    for (i, block) in blocks.into_iter().enumerate() {
        ctx.push(format!("content[{i}]"));

        let known = match block {
            AnthropicOutputContentBlock::Known(k) => k,
            AnthropicOutputContentBlock::Other(_) => {
                ctx.warn(
                    "content_block",
                    WarningAction::Dropped,
                    "unknown content block type",
                );
                ctx.pop();
                continue;
            }
        };

        match known {
            AnthropicKnownOutputContentBlock::Text { text, citations } => {
                convert_text_block(accum, text, citations, ctx);
            }
            AnthropicKnownOutputContentBlock::ToolUse { id, name, input } => {
                convert_tool_use_block(accum, id, name, input, ctx);
            }
            AnthropicKnownOutputContentBlock::Thinking {
                thinking,
                signature,
            } => {
                let id = accum
                    .generated_item_id_after_flush(OpenResponsesOutputItemKind::Reasoning, None);
                accum.push_flushed_item(OutputItem::Reasoning {
                    id,
                    summary: vec![ContentPart::SummaryText { text: thinking }],
                    content: None,
                    encrypted_content: Some(signature),
                });
            }
            AnthropicKnownOutputContentBlock::RedactedThinking { data } => {
                let id = accum
                    .generated_item_id_after_flush(OpenResponsesOutputItemKind::Reasoning, None);
                accum.push_flushed_item(OutputItem::Reasoning {
                    id,
                    summary: Vec::new(),
                    content: None,
                    encrypted_content: Some(data),
                });
            }
            AnthropicKnownOutputContentBlock::ServerToolUse {
                id, name, input, ..
            } => {
                if name == "web_search" {
                    let query = input
                        .get("query")
                        .and_then(|v| v.as_str())
                        .map(String::from);
                    pending_web_search = Some((id, query));
                } else if name.starts_with("tool_search_tool") {
                    pending_tool_search = Some((id, input));
                } else {
                    ctx.warn(
                        "server_tool_use",
                        WarningAction::Dropped,
                        format!("unsupported server tool '{name}'"),
                    );
                }
            }
            AnthropicKnownOutputContentBlock::WebSearchToolResult {
                tool_use_id,
                content,
            } => {
                let query = pending_web_search
                    .take()
                    .filter(|(id, _)| *id == tool_use_id)
                    .and_then(|(_, q)| q);

                let (status, sources) = convert_web_search_results(content, ctx);
                // Preserve the Anthropic tool-use id here: Open Responses
                // needs the web-search item id to correlate the server-tool
                // use with its later tool-result block during OR→AM round trips.
                accum.push_item(OutputItem::WebSearchCall {
                    id: tool_use_id,
                    status,
                    action: Some(WebSearchAction::Search {
                        query,
                        queries: vec![],
                        sources,
                    }),
                });
            }
            AnthropicKnownOutputContentBlock::ToolSearchToolResult {
                tool_use_id,
                content,
                ..
            } => {
                let (pending_id, arguments) = pending_tool_search.take().unwrap_or_else(|| {
                    (
                        tool_use_id.clone(),
                        serde_json::Value::Object(Default::default()),
                    )
                });
                match content {
                    AnthropicToolSearchToolResultContent::Error { error_code, .. } => {
                        ctx.warn(
                            "tool_search_tool_result",
                            WarningAction::Changed,
                            format!("tool_search_tool_result error: {error_code}"),
                        );
                        accum.push_item(OutputItem::ToolSearchCall {
                            id: pending_id,
                            call_id: None,
                            arguments,
                            execution: Some(ToolSearchExecution::Server),
                            status: ToolSearchCallStatus::Incomplete,
                        });
                    }
                    AnthropicToolSearchToolResultContent::SearchResult { tool_references } => {
                        let tools = tool_references_from_flat_names(
                            tool_references.into_iter().map(|r| r.tool_name),
                        );
                        accum.push_item(OutputItem::ToolSearchCall {
                            id: pending_id,
                            call_id: None,
                            arguments,
                            execution: Some(ToolSearchExecution::Server),
                            status: ToolSearchCallStatus::Completed,
                        });
                        // Preserve a deterministic relationship to the source
                        // tool result id; OR→AM conversion uses this id as the
                        // synthetic output item id while the call_id preserves
                        // the original Anthropic tool_use_id.
                        accum.push_item(OutputItem::ToolSearchOutput {
                            id: format!("{tool_use_id}_output"),
                            call_id: Some(tool_use_id),
                            tools,
                            execution: Some(ToolSearchExecution::Server),
                            status: ToolSearchCallStatus::Completed,
                        });
                    }
                }
            }
        }

        ctx.pop();
    }

    if let Some((id, query)) = pending_web_search {
        // Preserve the source server-tool id so orphaned/in-progress web search
        // calls can still be correlated if converted back to Anthropic.
        accum.push_item(OutputItem::WebSearchCall {
            id,
            status: WebSearchCallStatus::InProgress,
            action: Some(WebSearchAction::Search {
                query,
                queries: vec![],
                sources: vec![],
            }),
        });
    }

    if let Some((id, arguments)) = pending_tool_search.take() {
        accum.push_item(OutputItem::ToolSearchCall {
            id,
            call_id: None,
            arguments,
            execution: Some(ToolSearchExecution::Server),
            status: ToolSearchCallStatus::InProgress,
        });
    }

    accum.flush_message();
}

fn convert_text_block(
    accum: &mut OpenResponsesOutputAccum,
    text: String,
    citations: Vec<AnthropicCitation>,
    ctx: &mut ConversionCtx,
) {
    let annotations: Vec<Annotation> = citations
        .into_iter()
        .filter_map(|c| {
            let result = convert_anthropic_messages_citation_to_open_responses(c, &text, None);
            if result.is_none() {
                ctx.warn(
                    "citation",
                    WarningAction::Dropped,
                    "non-URL citation type or cited text not found",
                );
            }
            result
        })
        .collect();

    accum.push_content_part(ContentPart::OutputText {
        text,
        annotations,
        logprobs: vec![],
    });
}

fn convert_tool_use_block(
    accum: &mut OpenResponsesOutputAccum,
    id: String,
    name: String,
    input: serde_json::Value,
    ctx: &mut ConversionCtx,
) {
    // TODO: can arguments be something other than a JSON object? Investigate and handle other
    // cases if so
    let arguments = serde_json::to_string(&input).unwrap_or_else(|_| {
        ctx.warn(
            "tool_use.input",
            WarningAction::Changed,
            "failed to serialize tool input, replaced with empty string",
        );
        String::new()
    });
    let fc_id =
        accum.generated_item_id_after_flush(OpenResponsesOutputItemKind::FunctionCall, Some(&id));

    let (namespace, name) = split_tool_name(name);
    accum.push_flushed_item(OutputItem::FunctionCall {
        id: fc_id,
        call_id: id,
        name,
        namespace,
        arguments,
        status: ItemStatus::Completed,
    });
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn web_search_citation_converts_to_url_citation() {
        let citation = AnthropicCitation::WebSearchResultLocation {
            cited_text: "hello world".into(),
            encrypted_index: "enc".into(),
            title: "Example".into(),
            url: "https://example.com".into(),
        };
        let ann = convert_anthropic_messages_citation_to_open_responses(
            citation,
            "prefix hello world suffix",
            None,
        )
        .unwrap();
        match ann {
            Annotation::UrlCitation {
                url,
                title,
                start_index,
                end_index,
            } => {
                assert_eq!(url, "https://example.com");
                assert_eq!(title, "Example");
                assert_eq!(start_index, 7);
                assert_eq!(end_index, 18);
            }
        }
    }

    #[test]
    fn non_url_citation_returns_none() {
        let citation = AnthropicCitation::CharLocation {
            cited_text: "x".into(),
            document_index: 0,
            document_title: "t".into(),
            start_char_index: 0,
            end_char_index: 1,
        };
        assert!(
            convert_anthropic_messages_citation_to_open_responses(citation, "hi", None).is_none()
        );
    }

    #[test]
    fn usage_conversion_normalizes_input_tokens() {
        // Anthropic: input_tokens=100 (non-cached), cache_read=20
        // OR convention: input_tokens = total input = 100 + 20 = 120
        let am = AnthropicUsage {
            input_tokens: 100,
            output_tokens: 50,
            output_tokens_details: None,
            cache_creation_input_tokens: None,
            cache_read_input_tokens: Some(20),
            cache_creation: None,
            server_tool_use: None,
            service_tier: None,
            inference_geo: None,
        };
        let or = Usage::from(am);
        assert_eq!(or.input_tokens, 120);
        assert_eq!(or.output_tokens, 50);
        assert_eq!(or.total_tokens, 170);
        assert_eq!(or.input_tokens_details.unwrap().cached_tokens, 20);
    }

    #[test]
    fn usage_conversion_no_cache_passthrough() {
        // Without caching, input_tokens is passed through unchanged.
        let am = AnthropicUsage {
            input_tokens: 100,
            output_tokens: 50,
            output_tokens_details: None,
            cache_creation_input_tokens: None,
            cache_read_input_tokens: None,
            cache_creation: None,
            server_tool_use: None,
            service_tier: None,
            inference_geo: None,
        };
        let or = Usage::from(am);
        assert_eq!(or.input_tokens, 100);
        assert_eq!(or.output_tokens, 50);
        assert_eq!(or.total_tokens, 150);
        assert_eq!(or.input_tokens_details.unwrap().cached_tokens, 0);
        assert_eq!(or.output_tokens_details.unwrap().reasoning_tokens, 0);
    }

    #[test]
    fn usage_conversion_maps_thinking_tokens_to_reasoning_tokens() {
        let am = AnthropicUsage {
            input_tokens: 30,
            output_tokens: 124,
            output_tokens_details: Some(AnthropicOutputTokensDetails {
                thinking_tokens: 117,
            }),
            cache_creation_input_tokens: None,
            cache_read_input_tokens: None,
            cache_creation: None,
            server_tool_use: None,
            service_tier: None,
            inference_geo: None,
        };
        let or = Usage::from(am);
        assert_eq!(or.output_tokens, 124);
        assert_eq!(or.total_tokens, 154);
        assert_eq!(or.output_tokens_details.unwrap().reasoning_tokens, 117);
    }

    #[test]
    fn usage_conversion_includes_cache_creation_in_total_input() {
        let am = AnthropicUsage {
            input_tokens: 3,
            output_tokens: 4120,
            output_tokens_details: None,
            cache_creation_input_tokens: Some(23147),
            cache_read_input_tokens: Some(0),
            cache_creation: None,
            server_tool_use: None,
            service_tier: None,
            inference_geo: None,
        };
        let or = Usage::from(am);
        assert_eq!(or.input_tokens, 23150);
        assert_eq!(or.output_tokens, 4120);
        assert_eq!(or.total_tokens, 27270);
        assert_eq!(or.input_tokens_details.unwrap().cached_tokens, 0);
    }

    #[test]
    fn usage_conversion_sums_uncached_cache_read_and_cache_creation_tokens() {
        let am = AnthropicUsage {
            input_tokens: 100,
            output_tokens: 50,
            output_tokens_details: None,
            cache_creation_input_tokens: Some(200),
            cache_read_input_tokens: Some(300),
            cache_creation: None,
            server_tool_use: None,
            service_tier: None,
            inference_geo: None,
        };
        let or = Usage::from(am);
        assert_eq!(or.input_tokens, 600);
        assert_eq!(or.output_tokens, 50);
        assert_eq!(or.total_tokens, 650);
        assert_eq!(or.input_tokens_details.unwrap().cached_tokens, 300);
    }

    #[test]
    fn usage_conversion_heavy_caching_no_negative() {
        // The scenario that caused the original bug: cache_read >> input_tokens.
        // Anthropic: input_tokens=10 (non-cached), cache_read=1000
        // OR: input_tokens should be 1010, never negative.
        let am = AnthropicUsage {
            input_tokens: 10,
            output_tokens: 25,
            output_tokens_details: None,
            cache_creation_input_tokens: None,
            cache_read_input_tokens: Some(1000),
            cache_creation: None,
            server_tool_use: None,
            service_tier: None,
            inference_geo: None,
        };
        let or = Usage::from(am);
        assert_eq!(or.input_tokens, 1010);
        assert_eq!(or.output_tokens, 25);
        assert_eq!(or.total_tokens, 1035);
        let details = or.input_tokens_details.unwrap();
        assert_eq!(details.cached_tokens, 1000);
        assert!(or.input_tokens >= details.cached_tokens);
    }

    #[test]
    fn usage_round_trip_preserves_anthropic_values() {
        // AM → OR → AM should recover the original Anthropic values.
        let original = AnthropicUsage {
            input_tokens: 10,
            output_tokens: 25,
            output_tokens_details: None,
            cache_creation_input_tokens: None,
            cache_read_input_tokens: Some(1000),
            cache_creation: None,
            server_tool_use: None,
            service_tier: None,
            inference_geo: None,
        };
        let or = Usage::from(original.clone());
        let back = AnthropicUsage::from(or);
        assert_eq!(back.input_tokens, original.input_tokens);
        assert_eq!(back.output_tokens, original.output_tokens);
        assert_eq!(
            back.cache_read_input_tokens,
            original.cache_read_input_tokens
        );
    }

    #[test]
    fn usage_roundtrip_preserves_cache_creation() {
        let usage = Usage {
            input_tokens: 600,
            output_tokens: 50,
            total_tokens: 650,
            input_tokens_details: Some(InputTokensDetails {
                cached_tokens: 300,
                cache_write_tokens: Some(200),
            }),
            output_tokens_details: Some(OutputTokensDetails {
                reasoning_tokens: 0,
            }),
        };

        let anthropic = AnthropicUsage::from(usage.clone());
        assert_eq!(anthropic.input_tokens, 100);
        assert_eq!(anthropic.output_tokens, 50);
        assert_eq!(anthropic.cache_read_input_tokens, Some(300));
        assert_eq!(anthropic.cache_creation_input_tokens, Some(200));
        assert!(anthropic.output_tokens_details.is_none());
        assert_eq!(
            anthropic.input_tokens
                + anthropic.cache_read_input_tokens.unwrap_or(0)
                + anthropic.cache_creation_input_tokens.unwrap_or(0),
            usage.input_tokens
        );

        let round_tripped = Usage::from(anthropic);
        assert_eq!(round_tripped.input_tokens, usage.input_tokens);
        assert_eq!(round_tripped.output_tokens, usage.output_tokens);
        assert_eq!(round_tripped.total_tokens, usage.total_tokens);
        let details = round_tripped.input_tokens_details.unwrap();
        assert_eq!(details.cached_tokens, 300);
        assert_eq!(details.cache_write_tokens, Some(200));
    }

    #[test]
    fn usage_roundtrip_preserves_nonzero_reasoning_tokens() {
        let usage = Usage {
            input_tokens: 30,
            output_tokens: 124,
            total_tokens: 154,
            input_tokens_details: Some(InputTokensDetails {
                cached_tokens: 0,
                cache_write_tokens: None,
            }),
            output_tokens_details: Some(OutputTokensDetails {
                reasoning_tokens: 117,
            }),
        };

        let anthropic = AnthropicUsage::from(usage.clone());
        assert_eq!(
            anthropic
                .output_tokens_details
                .as_ref()
                .unwrap()
                .thinking_tokens,
            117
        );

        let round_tripped = Usage::from(anthropic);
        assert_eq!(
            round_tripped
                .output_tokens_details
                .unwrap()
                .reasoning_tokens,
            117
        );
    }

    #[test]
    fn stop_reason_end_turn_maps_to_completed() {
        let (status, details) = convert_anthropic_messages_stop_reason_to_open_responses(Some(
            AnthropicStopReason::EndTurn,
        ));
        assert_eq!(status, ResponseStatus::Completed);
        assert!(details.is_none());
    }

    #[test]
    fn stop_reason_max_tokens_maps_to_incomplete() {
        let (status, details) = convert_anthropic_messages_stop_reason_to_open_responses(Some(
            AnthropicStopReason::MaxTokens,
        ));
        assert_eq!(status, ResponseStatus::Incomplete);
        assert_eq!(details.unwrap().reason, "max_output_tokens");
    }
}
