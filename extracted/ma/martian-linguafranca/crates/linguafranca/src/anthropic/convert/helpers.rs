use crate::anthropic::types::*;
use crate::error::WarningAction;
use crate::open_responses::response::OpenResponsesResponse;
use crate::open_responses::types::*;

pub fn image_source_to_url(source: ImageSource) -> String {
    match source {
        ImageSource::Base64 { data, media_type } => format!("data:{media_type};base64,{data}"),
        ImageSource::Url { url } => url,
    }
}

/// Returns `(ImageSource, warning_message)`. The warning is `Some` when the
/// data URL is malformed (missing `;base64,` segment).
pub fn url_to_image_source(url: String) -> (ImageSource, Option<String>) {
    if url.starts_with("data:") {
        let after_data = url.strip_prefix("data:").unwrap_or("");
        if let Some((media_type, data)) = after_data.split_once(";base64,") {
            (
                ImageSource::Base64 {
                    data: data.to_string(),
                    media_type: media_type.to_string(),
                },
                None,
            )
        } else {
            (
                ImageSource::Base64 {
                    data: String::new(),
                    media_type: "application/octet-stream".into(),
                },
                Some("malformed data URL: missing ;base64, segment, using empty data".into()),
            )
        }
    } else {
        (ImageSource::Url { url }, None)
    }
}

pub fn document_source_to_open_responses_file(
    source: DocumentSource,
    title: Option<String>,
) -> InputContentPart {
    match source {
        DocumentSource::Url { url } => InputContentPart::File {
            filename: title,
            file_data: None,
            file_url: Some(url),
        },
        DocumentSource::Base64 { data, .. } | DocumentSource::PlainText { data, .. } => {
            InputContentPart::File {
                filename: title,
                file_data: Some(data),
                file_url: None,
            }
        }
        DocumentSource::Content { content } => match content {
            AnthropicDocumentContent::Text(t) => InputContentPart::Text { text: t },
            AnthropicDocumentContent::Blocks(blocks) => {
                let text = blocks
                    .into_iter()
                    .filter_map(|b| match b {
                        AnthropicInputContentBlock::Text { text, .. } => Some(text),
                        _ => None,
                    })
                    .collect::<Vec<_>>()
                    .join("\n");
                InputContentPart::Text { text }
            }
        },
    }
}

// TODO: consider using tool output blocks for richer search result representation
pub fn search_result_to_text(
    title: String,
    content: Vec<AnthropicSearchResultText>,
) -> InputContentPart {
    let text = std::iter::once(title)
        .chain(content.into_iter().map(|b| b.text))
        .collect::<Vec<_>>()
        .join("\n");
    InputContentPart::Text { text }
}

pub fn open_responses_file_to_document_source(
    file_url: Option<String>,
    file_data: Option<String>,
    filename: Option<&str>,
) -> Option<DocumentSource> {
    match (file_url, file_data) {
        (Some(url), _) => Some(DocumentSource::Url { url }),
        (None, Some(data)) => {
            let media_type = filename
                .map(guess_media_type)
                .unwrap_or_else(|| "text/plain".into());
            Some(DocumentSource::Base64 { data, media_type })
        }
        (None, None) => None,
    }
}

// TODO: rework to properly identify file type — OR doesn't carry media type info,
// so we rely on extension guessing which is fragile and defaults to text/plain.
pub fn guess_media_type(name: &str) -> String {
    let path = name.split('?').next().unwrap_or(name);
    match path.rsplit_once('.').map(|(_, ext)| ext) {
        Some("pdf") => "application/pdf",
        Some("txt" | "md" | "csv" | "json" | "xml" | "html") => "text/plain",
        _ => "text/plain",
    }
    .into()
}

// ── Response / stream shared helpers ──

pub(crate) fn convert_anthropic_messages_citation_to_open_responses(
    citation: AnthropicCitation,
    generated_text: &str,
    fallback_span: Option<(u64, u64)>,
) -> Option<Annotation> {
    match citation {
        AnthropicCitation::WebSearchResultLocation {
            url,
            title,
            cited_text,
            ..
        } => {
            let (start_index, end_index) =
                citation_span(&cited_text, generated_text, fallback_span)?;
            Some(Annotation::UrlCitation {
                url,
                title,
                start_index,
                end_index,
            })
        }
        _ => None,
    }
}

fn citation_span(
    cited_text: &str,
    generated_text: &str,
    fallback_span: Option<(u64, u64)>,
) -> Option<(u64, u64)> {
    let text_len = char_len(generated_text);
    exact_generated_text_span(
        cited_text,
        generated_text,
        fallback_span.map(|(start, _)| start),
    )
    .or_else(|| fallback_span.and_then(|(start, end)| clamp_span(start, end, text_len)))
    .or_else(|| (text_len > 0).then_some((0, text_len)))
}

fn exact_generated_text_span(
    cited_text: &str,
    generated_text: &str,
    preferred_start: Option<u64>,
) -> Option<(u64, u64)> {
    if cited_text.is_empty() {
        return None;
    }

    if let Some(start) = preferred_start
        && let Some(byte_offset) = byte_offset_for_char_index(generated_text, start)
        && let Some(relative_start) = generated_text[byte_offset..].find(cited_text)
    {
        let byte_start = byte_offset + relative_start;
        return Some(span_from_byte_start(cited_text, generated_text, byte_start));
    }

    let byte_start = generated_text.find(cited_text)?;
    Some(span_from_byte_start(cited_text, generated_text, byte_start))
}

fn span_from_byte_start(cited_text: &str, generated_text: &str, byte_start: usize) -> (u64, u64) {
    let start = char_len(&generated_text[..byte_start]);
    let end = start + char_len(cited_text);
    (start, end)
}

fn byte_offset_for_char_index(text: &str, char_index: u64) -> Option<usize> {
    let target = usize::try_from(char_index).ok()?;
    if target == char_len(text) as usize {
        return Some(text.len());
    }
    text.char_indices().nth(target).map(|(idx, _)| idx)
}

fn char_len(text: &str) -> u64 {
    text.chars().count() as u64
}

fn clamp_span(start: u64, end: u64, text_len: u64) -> Option<(u64, u64)> {
    if text_len == 0 {
        return None;
    }
    let start = start.min(text_len);
    let end = end.min(text_len).max(start);
    Some((start, end))
}

pub(crate) fn convert_open_responses_annotation_to_anthropic_messages(
    ann: Annotation,
) -> AnthropicCitation {
    match ann {
        Annotation::UrlCitation { url, title, .. } => AnthropicCitation::WebSearchResultLocation {
            cited_text: String::new(),
            encrypted_index: String::new(),
            title,
            url,
        },
    }
}

impl From<AnthropicUsage> for Usage {
    fn from(usage: AnthropicUsage) -> Self {
        // Anthropic splits prompt tokens into uncached, cache-read, and cache-creation
        // buckets. Open Responses' top-level `input_tokens` is closer to total input
        // scope, so include all three buckets here and preserve cache creation in
        // `input_tokens_details.cache_write_tokens`.
        let cached = usage.cache_read_input_tokens.unwrap_or(0);
        let cache_creation = usage.cache_creation_input_tokens.unwrap_or(0);
        let reasoning_tokens = usage
            .output_tokens_details
            .as_ref()
            .map(|details| details.thinking_tokens)
            .unwrap_or(0);
        let total_input = usage.input_tokens + cached + cache_creation;
        Self {
            input_tokens: total_input,
            output_tokens: usage.output_tokens,
            total_tokens: total_input + usage.output_tokens,
            input_tokens_details: Some(InputTokensDetails {
                cached_tokens: cached,
                cache_write_tokens: usage
                    .cache_creation_input_tokens
                    .filter(|tokens| *tokens > 0),
            }),
            output_tokens_details: Some(OutputTokensDetails { reasoning_tokens }),
        }
    }
}

impl From<Usage> for AnthropicUsage {
    fn from(usage: Usage) -> Self {
        // Reverse of the normalization above: Anthropic expects `input_tokens`
        // to exclude cached tokens.
        //
        let details = usage.input_tokens_details;
        let cached = details.as_ref().map(|d| d.cached_tokens).unwrap_or(0);
        let cache_write = details
            .as_ref()
            .and_then(|d| d.cache_write_tokens)
            .filter(|tokens| *tokens > 0);
        let output_tokens_details = usage.output_tokens_details.and_then(|details| {
            (details.reasoning_tokens > 0).then_some(AnthropicOutputTokensDetails {
                thinking_tokens: details.reasoning_tokens,
            })
        });
        Self {
            input_tokens: usage
                .input_tokens
                .saturating_sub(cached)
                .saturating_sub(cache_write.unwrap_or(0)),
            output_tokens: usage.output_tokens,
            output_tokens_details,
            cache_read_input_tokens: details.as_ref().map(|d| d.cached_tokens),
            cache_creation_input_tokens: cache_write,
            ..Default::default()
        }
    }
}

pub(crate) fn convert_anthropic_messages_stop_reason_to_open_responses(
    reason: Option<AnthropicStopReason>,
) -> (ResponseStatus, Option<IncompleteDetails>) {
    match reason {
        None
        | Some(AnthropicStopReason::EndTurn)
        | Some(AnthropicStopReason::ToolUse)
        | Some(AnthropicStopReason::Refusal) => (ResponseStatus::Completed, None),
        Some(AnthropicStopReason::MaxTokens) => (
            ResponseStatus::Incomplete,
            Some(IncompleteDetails {
                reason: "max_output_tokens".into(),
            }),
        ),
        Some(AnthropicStopReason::StopSequence) => (
            ResponseStatus::Incomplete,
            Some(IncompleteDetails {
                reason: "stop_sequence".into(),
            }),
        ),
        Some(AnthropicStopReason::PauseTurn) => (
            ResponseStatus::Incomplete,
            Some(IncompleteDetails {
                reason: "pause_turn".into(),
            }),
        ),
    }
}

pub(crate) fn convert_open_responses_status_to_anthropic_messages_stop_reason(
    status: ResponseStatus,
    output: &[OutputItem],
    incomplete_details: Option<&IncompleteDetails>,
) -> Option<AnthropicStopReason> {
    match status {
        ResponseStatus::Completed => {
            let last_is_function_call = output
                .last()
                .is_some_and(|item| matches!(item, OutputItem::FunctionCall { .. }));
            if last_is_function_call {
                Some(AnthropicStopReason::ToolUse)
            } else {
                Some(AnthropicStopReason::EndTurn)
            }
        }
        ResponseStatus::Incomplete => match incomplete_details.map(|d| d.reason.as_str()) {
            Some("stop_sequence") => Some(AnthropicStopReason::StopSequence),
            Some("pause_turn") => Some(AnthropicStopReason::PauseTurn),
            _ => Some(AnthropicStopReason::MaxTokens),
        },
        ResponseStatus::Failed => Some(AnthropicStopReason::EndTurn),
        ResponseStatus::InProgress | ResponseStatus::Queued => None,
    }
}

pub(crate) fn build_open_responses_response_snapshot(
    id: String,
    model: String,
    status: ResponseStatus,
    output: Vec<OutputItem>,
    usage: Option<Usage>,
    incomplete_details: Option<IncompleteDetails>,
    service_tier: Option<ServiceTier>,
) -> OpenResponsesResponse {
    OpenResponsesResponse {
        id,
        object: "response".into(),
        // TODO: AM doesn't return a timestamp — consider using current time here
        created_at: 0,
        status,
        model,
        output,
        usage,
        incomplete_details,
        service_tier,
        ..Default::default()
    }
}

pub(crate) fn convert_web_search_results(
    content: Vec<AnthropicWebSearchToolResultItem>,
    ctx: &mut crate::anthropic::convert::ctx::ConversionCtx,
) -> (WebSearchCallStatus, Vec<WebSearchSource>) {
    let has_error = content
        .iter()
        .any(|item| matches!(item, AnthropicWebSearchToolResultItem::Error { .. }));
    if has_error {
        return (WebSearchCallStatus::Failed, vec![]);
    }
    let sources = content
        .into_iter()
        .filter_map(|item| match item {
            AnthropicWebSearchToolResultItem::WebSearchResult {
                url,
                title,
                encrypted_content,
                page_age,
            } => {
                if !title.is_empty() {
                    ctx.warn(
                        "web_search_result.title",
                        WarningAction::Dropped,
                        "not supported in Open Responses",
                    );
                }
                if !encrypted_content.is_empty() {
                    ctx.warn(
                        "web_search_result.encrypted_content",
                        WarningAction::Dropped,
                        "not supported in Open Responses",
                    );
                }
                if page_age.is_some() {
                    ctx.warn(
                        "web_search_result.page_age",
                        WarningAction::Dropped,
                        "not supported in Open Responses",
                    );
                }
                Some(WebSearchSource {
                    source_type: "url".into(),
                    url,
                })
            }
            _ => None,
        })
        .collect();
    (WebSearchCallStatus::Completed, sources)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn valid_data_url_parses_without_warning() {
        let (source, warn) = url_to_image_source("data:image/png;base64,iVBORw0KGgo=".into());
        assert!(warn.is_none());
        match source {
            ImageSource::Base64 { data, media_type } => {
                assert_eq!(media_type, "image/png");
                assert_eq!(data, "iVBORw0KGgo=");
            }
            other => panic!("expected Base64, got {other:?}"),
        }
    }

    #[test]
    fn malformed_data_url_returns_warning() {
        let (source, warn) = url_to_image_source("data:not-valid-at-all".into());
        assert!(warn.is_some());
        assert!(warn.unwrap().contains("malformed"));
        match source {
            ImageSource::Base64 { data, media_type } => {
                assert!(data.is_empty());
                assert_eq!(media_type, "application/octet-stream");
            }
            other => panic!("expected Base64, got {other:?}"),
        }
    }

    #[test]
    fn regular_url_passes_through() {
        let (source, warn) = url_to_image_source("https://example.com/img.png".into());
        assert!(warn.is_none());
        match source {
            ImageSource::Url { url } => assert_eq!(url, "https://example.com/img.png"),
            other => panic!("expected Url, got {other:?}"),
        }
    }

    #[test]
    fn web_search_citation_end_index_counts_chars_not_bytes() {
        let ann = convert_anthropic_messages_citation_to_open_responses(
            AnthropicCitation::WebSearchResultLocation {
                cited_text: "résumé".into(),
                encrypted_index: "enc".into(),
                title: "Example".into(),
                url: "https://example.com".into(),
            },
            "See résumé for details",
            None,
        )
        .unwrap();

        assert_eq!(
            ann,
            Annotation::UrlCitation {
                url: "https://example.com".into(),
                title: "Example".into(),
                start_index: 4,
                end_index: 10,
            }
        );
    }

    #[test]
    fn web_search_citation_falls_back_to_generated_text_span() {
        let ann = convert_anthropic_messages_citation_to_open_responses(
            AnthropicCitation::WebSearchResultLocation {
                cited_text: "source-page quote".into(),
                encrypted_index: "enc".into(),
                title: "Example".into(),
                url: "https://example.com".into(),
            },
            "generated answer",
            None,
        )
        .unwrap();

        assert_eq!(
            ann,
            Annotation::UrlCitation {
                url: "https://example.com".into(),
                title: "Example".into(),
                start_index: 0,
                end_index: 16,
            }
        );
    }

    #[test]
    fn web_search_citation_returns_none_when_no_span_available() {
        assert!(
            convert_anthropic_messages_citation_to_open_responses(
                AnthropicCitation::WebSearchResultLocation {
                    cited_text: "missing".into(),
                    encrypted_index: "enc".into(),
                    title: "Example".into(),
                    url: "https://example.com".into(),
                },
                "",
                None,
            )
            .is_none()
        );
    }

    #[test]
    fn web_search_citation_prefers_match_at_fallback_start() {
        let ann = convert_anthropic_messages_citation_to_open_responses(
            AnthropicCitation::WebSearchResultLocation {
                cited_text: "source".into(),
                encrypted_index: "enc".into(),
                title: "Example".into(),
                url: "https://example.com".into(),
            },
            "source then later source",
            Some((12, 23)),
        )
        .unwrap();

        assert_eq!(
            ann,
            Annotation::UrlCitation {
                url: "https://example.com".into(),
                title: "Example".into(),
                start_index: 18,
                end_index: 24,
            }
        );
    }

    #[test]
    fn image_source_roundtrip() {
        let original = "data:image/jpeg;base64,/9j/4AAQ";
        let (source, _) = url_to_image_source(original.into());
        let url = image_source_to_url(source);
        assert_eq!(url, original);
    }
}
