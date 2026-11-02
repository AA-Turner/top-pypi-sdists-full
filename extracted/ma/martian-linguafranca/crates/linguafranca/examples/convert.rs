use linguafranca::anthropic::convert::stream::{
    AnthropicMessagesToOpenResponsesStream, OpenResponsesToAnthropicMessagesStream,
};
use linguafranca::anthropic::request::AnthropicRequest;
use linguafranca::anthropic::response::AnthropicResponse;
use linguafranca::chat_completions_openai::convert::stream::{
    ChatCompletionsToOpenResponsesStream, OpenResponsesToChatCompletionsStream,
};
use linguafranca::chat_completions_openai::request::ChatCompletionsOpenAiRequest;
use linguafranca::chat_completions_openai::response::ChatCompletionsOpenAiResponse;
use linguafranca::error::ConversionResult;
use linguafranca::open_responses::request::OpenResponsesRequest;
use linguafranca::open_responses::response::OpenResponsesResponse;
use linguafranca::stream::StreamTransform;
use linguafranca::traits::{FromOpenResponses, IntoOpenResponses};

fn print_result<T: serde::Serialize>(result: ConversionResult<T>) {
    println!("{}", serde_json::to_string_pretty(&result.value).unwrap());
    if !result.warnings.is_empty() {
        eprintln!("\nWarnings:");
        for w in &result.warnings {
            eprintln!("  [{}] {}", w.field, w.message);
        }
    }
}

fn into_or<S: serde::de::DeserializeOwned + IntoOpenResponses>(
    json: &str,
) -> ConversionResult<S::Target> {
    let source: S = serde_json::from_str(json).expect("failed to parse input");
    source
        .into_open_responses(None)
        .expect("into_open_responses failed")
}

fn from_or<T: FromOpenResponses + serde::Serialize>(or: ConversionResult<T::Source>) {
    let mut result = T::from_open_responses(or.value, None).expect("from_open_responses failed");
    result.warnings.splice(0..0, or.warnings);
    print_result(result);
}

fn run_stream<S: StreamTransform>(json: &str, mut stream: S)
where
    S::Input: serde::de::DeserializeOwned,
    S::Output: serde::Serialize,
{
    let events: Vec<S::Input> = match serde_json::from_str::<serde_json::Value>(json) {
        Ok(serde_json::Value::Array(_)) => {
            serde_json::from_str(json).expect("failed to parse events array")
        }
        Ok(_) => vec![serde_json::from_str(json).expect("failed to parse single event")],
        Err(e) => panic!("failed to parse: {e}"),
    };

    let mut outputs = Vec::new();
    for (i, event) in events.into_iter().enumerate() {
        match stream.transform(event) {
            Ok(out) => outputs.extend(out),
            Err(e) => eprintln!("transform error at event #{i}: {e}"),
        }
    }
    match stream.flush() {
        Ok(out) => outputs.extend(out),
        Err(e) => eprintln!("flush error: {e}"),
    }

    println!("{}", serde_json::to_string_pretty(&outputs).unwrap());

    let warnings = stream.take_warnings();
    if !warnings.is_empty() {
        eprintln!("\nWarnings:");
        for w in &warnings {
            eprintln!("  [{}] {}", w.field, w.message);
        }
    }
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    if args.len() < 4 {
        eprintln!("Usage: convert <source> <target> <request|response|stream> [file]");
        eprintln!("Formats: or, cc, am");
        std::process::exit(1);
    }

    let source = &args[1];
    let target = &args[2];
    let kind = &args[3];
    let path = args.get(4).map(|s| s.as_str()).unwrap_or("test.json");
    let json = std::fs::read_to_string(path).expect("failed to read file");

    match (source.as_str(), target.as_str(), kind.as_str()) {
        // Request conversions
        ("or", "cc", "request") => {
            let or: OpenResponsesRequest = serde_json::from_str(&json).expect("failed to parse");
            from_or::<ChatCompletionsOpenAiRequest>(ConversionResult {
                value: or,
                warnings: vec![],
            });
        }
        ("or", "am", "request") => {
            let or: OpenResponsesRequest = serde_json::from_str(&json).expect("failed to parse");
            from_or::<AnthropicRequest>(ConversionResult {
                value: or,
                warnings: vec![],
            });
        }
        ("cc", "or", "request") => {
            let or = into_or::<ChatCompletionsOpenAiRequest>(&json);
            print_result(or);
        }
        ("cc", "am", "request") => {
            let or = into_or::<ChatCompletionsOpenAiRequest>(&json);
            from_or::<AnthropicRequest>(or);
        }
        ("am", "or", "request") => {
            let or = into_or::<AnthropicRequest>(&json);
            print_result(or);
        }
        ("am", "cc", "request") => {
            let or = into_or::<AnthropicRequest>(&json);
            from_or::<ChatCompletionsOpenAiRequest>(or);
        }
        ("or", "or", "request") => {
            let v: OpenResponsesRequest = serde_json::from_str(&json).expect("failed to parse");
            print_result(ConversionResult {
                value: v,
                warnings: vec![],
            });
        }
        ("cc", "cc", "request") => {
            let v: ChatCompletionsOpenAiRequest =
                serde_json::from_str(&json).expect("failed to parse");
            print_result(ConversionResult {
                value: v,
                warnings: vec![],
            });
        }
        ("am", "am", "request") => {
            let v: AnthropicRequest = serde_json::from_str(&json).expect("failed to parse");
            print_result(ConversionResult {
                value: v,
                warnings: vec![],
            });
        }

        // Response conversions
        ("or", "cc", "response") => {
            let or: OpenResponsesResponse = serde_json::from_str(&json).expect("failed to parse");
            from_or::<ChatCompletionsOpenAiResponse>(ConversionResult {
                value: or,
                warnings: vec![],
            });
        }
        ("or", "am", "response") => {
            let or: OpenResponsesResponse = serde_json::from_str(&json).expect("failed to parse");
            from_or::<AnthropicResponse>(ConversionResult {
                value: or,
                warnings: vec![],
            });
        }
        ("cc", "or", "response") => {
            let or = into_or::<ChatCompletionsOpenAiResponse>(&json);
            print_result(or);
        }
        ("cc", "am", "response") => {
            let or = into_or::<ChatCompletionsOpenAiResponse>(&json);
            from_or::<AnthropicResponse>(or);
        }
        ("am", "or", "response") => {
            let or = into_or::<AnthropicResponse>(&json);
            print_result(or);
        }
        ("am", "cc", "response") => {
            let or = into_or::<AnthropicResponse>(&json);
            from_or::<ChatCompletionsOpenAiResponse>(or);
        }
        ("or", "or", "response") => {
            let v: OpenResponsesResponse = serde_json::from_str(&json).expect("failed to parse");
            print_result(ConversionResult {
                value: v,
                warnings: vec![],
            });
        }
        ("cc", "cc", "response") => {
            let v: ChatCompletionsOpenAiResponse =
                serde_json::from_str(&json).expect("failed to parse");
            print_result(ConversionResult {
                value: v,
                warnings: vec![],
            });
        }
        ("am", "am", "response") => {
            let v: AnthropicResponse = serde_json::from_str(&json).expect("failed to parse");
            print_result(ConversionResult {
                value: v,
                warnings: vec![],
            });
        }

        // Stream conversions (single event or array of events)
        ("or", "cc", "stream") => run_stream(&json, OpenResponsesToChatCompletionsStream::new()),
        ("or", "am", "stream") => run_stream(&json, OpenResponsesToAnthropicMessagesStream::new()),
        ("cc", "or", "stream") => run_stream(&json, ChatCompletionsToOpenResponsesStream::new()),
        ("am", "or", "stream") => run_stream(&json, AnthropicMessagesToOpenResponsesStream::new()),

        _ => {
            eprintln!("Unknown combination: {source} -> {target} ({kind})");
            eprintln!(
                "Formats: or (Open Responses), cc (Chat Completions), am (Anthropic Messages)"
            );
            eprintln!("Kinds: request, response, stream");
            std::process::exit(1);
        }
    }
}
