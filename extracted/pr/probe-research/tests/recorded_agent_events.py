"""Event lines the real agents printed on prbe-devbox, 2026-10-25.

Recorded with codex-cli 0.164.0 (`codex exec --json`, a ChatGPT account) and
Claude Code 2.1.296 (`claude -p --output-format stream-json --verbose`). Codex
lines are verbatim. Claude lines are trimmed to the fields an import reads (the
originals also carry local paths and plugin lists); every kept value is
verbatim. The non-JSON line is what Claude printed between them.
"""

from __future__ import annotations

#: `codex exec -m not-a-real-model-xyz`: exit 1 after about 4 s.
CODEX_BAD_MODEL = [
    '{"type":"thread.started","thread_id":"01a17647-1cd3-74f1-80f9-18d26af064ba"}',
    '{"type":"item.completed","item":{"id":"item_0","type":"error","message":"Model metadata for `not-a-real-model-xyz` not found. Defaulting to fallback metadata; this can degrade performance and cause issues."}}',
    '{"type":"turn.started"}',
    '{"type":"error","message":"{\\"type\\":\\"error\\",\\"status\\":400,\\"error\\":{\\"type\\":\\"invalid_request_error\\",\\"message\\":\\"The \'not-a-real-model-xyz\' model is not supported when using Codex with a ChatGPT account.\\",\\"code\\":\\"model_not_found\\"}}"}',
    '{"type":"turn.failed","error":{"message":"{\\"type\\":\\"error\\",\\"status\\":400,\\"error\\":{\\"type\\":\\"invalid_request_error\\",\\"message\\":\\"The \'not-a-real-model-xyz\' model is not supported when using Codex with a ChatGPT account.\\",\\"code\\":\\"model_not_found\\"}}"}}',
]

#: `codex exec -c model_reasoning_effort="bogus"`: exit 1.
CODEX_BAD_EFFORT = [
    '{"type":"thread.started","thread_id":"01a17647-3c7d-7ba1-913a-81daebaadd69"}',
    '{"type":"turn.started"}',
    '{"type":"error","message":"{\\"type\\":\\"error\\",\\"error\\":{\\"message\\":\\"Invalid response.create payload: Invalid value: \'bogus\'. Supported values are: \'none\', \'minimal\', \'low\', \'medium\', \'high\', \'xhigh\', and \'max\'.\\",\\"type\\":\\"invalid_request_error\\",\\"param\\":null,\\"code\\":null},\\"status\\":400}"}',
    '{"type":"turn.failed","error":{"message":"{\\"type\\":\\"error\\",\\"error\\":{\\"message\\":\\"Invalid response.create payload: Invalid value: \'bogus\'. Supported values are: \'none\', \'minimal\', \'low\', \'medium\', \'high\', \'xhigh\', and \'max\'.\\",\\"type\\":\\"invalid_request_error\\",\\"param\\":null,\\"code\\":null},\\"status\\":400}"}}',
]

#: `codex exec -c model_reasoning_effort="medium"`, "Reply with the single word ok.": exit 0.
CODEX_OK = [
    '{"type":"thread.started","thread_id":"01a17647-69ca-79e3-8136-ecd6d667e874"}',
    '{"type":"turn.started"}',
    '{"type":"item.completed","item":{"id":"item_0","type":"agent_message","text":"ok"}}',
    '{"type":"turn.completed","usage":{"input_tokens":30047,"cached_input_tokens":12288,"cache_write_input_tokens":0,"output_tokens":5,"reasoning_output_tokens":0}}',
]

#: `claude -p --model not-a-real-model-xyz`: exit 1.
CLAUDE_BAD_MODEL = [
    '{"type":"system","subtype":"init","session_id":"85f4e218-1808-449d-a6b2-6ffbdf9fcf0c","model":"not-a-real-model-xyz","claude_code_version":"2.1.296"}',
    '[claude-code:unrecognized_model] {"model":"not-a-real-model-xyz","query_source":"sdk"}',
    '{"type": "assistant", "message": {"model": "<synthetic>", "role": "assistant", "content": [{"type": "text", "text": "There\'s an issue with the selected model (not-a-real-model-xyz). It may not exist or you may not have access to it. Run --model to pick a different model."}], "usage": {"input_tokens": 0, "output_tokens": 0, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0}}, "session_id": "85f4e218-1808-449d-a6b2-6ffbdf9fcf0c"}',
    '{"type": "result", "subtype": "success", "is_error": true, "api_error_status": 404, "num_turns": 1, "result": "There\'s an issue with the selected model (not-a-real-model-xyz). It may not exist or you may not have access to it. Run --model to pick a different model.", "stop_reason": "stop_sequence", "session_id": "85f4e218-1808-449d-a6b2-6ffbdf9fcf0c", "terminal_reason": "api_error", "usage": {"input_tokens": 0, "cache_creation_input_tokens": 0, "cache_read_input_tokens": 0, "output_tokens": 0, "output_tokens_details": {"thinking_tokens": 0}}}',
]

#: `claude -p --model haiku --effort low`, "Reply with the single word ok.": exit 0.
CLAUDE_OK = [
    '{"type": "result", "subtype": "success", "is_error": false, "api_error_status": null, "num_turns": 1, "result": "ok", "stop_reason": "end_turn", "session_id": "9bd170db-8502-4d04-9cba-12f1c0ec19a5", "terminal_reason": "completed", "usage": {"input_tokens": 2, "cache_creation_input_tokens": 31298, "cache_read_input_tokens": 0, "output_tokens": 4, "output_tokens_details": {"thinking_tokens": 0}}}',
]
