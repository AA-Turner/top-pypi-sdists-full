#!/bin/bash
# Runlayer Hook - Unified MCP enforcement + raw event forwarding
# Auto-detects Cursor vs Claude Code vs Codex and adapts I/O format accordingly.
#
# Detection:
#   CURSOR_VERSION env var -> Cursor
#   ~/.codex or /etc/codex hook install path -> Codex
#   fallback -> Claude Code
#
# Enforcement events (blocking, when enforcement=true):
#   beforeMCPExecution (Cursor-only): resolve url/name command, forward to /hooks/cursor
#   PreToolUse / preToolUse:
#     - MCP tools (mcp__*): Claude Code and Codex resolve client MCP config, then enforce
#     - Read tool: local file path pattern matching for .env / MCP configs
#     - Native/local tools: synchronously forward to /hooks/tool/pre
#   PostToolUse / postToolUse:
#     - Native/local tools: synchronously forward to /hooks/tool/post
#   beforeReadFile / beforeTabFileRead (Cursor-only): local file path pattern matching
# Stop events: fire-and-forget with transcript (when available)
# All other events: fire-and-forget forwarding of raw payload to /hooks/events

set -euo pipefail

for _dir in "$HOME/.local/bin" /opt/homebrew/bin /usr/local/bin; do
  case ":${PATH}:" in *":${_dir}:"*) ;; *) PATH="${_dir}:${PATH}" ;; esac
done
export PATH

# =============================================================================
# Client detection
# =============================================================================
_CLIENT="claude_code"
_hook_dir_lower=$(dirname "$0" | tr '[:upper:]' '[:lower:]')
if [[ -n "${CURSOR_VERSION:-}" ]]; then
  _CLIENT="cursor"
elif [[ "$_hook_dir_lower" == */.hermes/* ]]; then
  _CLIENT="hermes"
elif [[ "$_hook_dir_lower" == */.codex/* ]] \
   || [[ "$_hook_dir_lower" == /etc/codex/* ]]; then
  _CLIENT="codex"
fi

# If Cursor loaded this hook from a non-Cursor config (e.g. ~/.claude/settings.json),
# no-op to avoid double enforcement with the Cursor-native hook.
# Match the actual Cursor config dirs, not bare "cursor" (avoids false positives
# when the OS username happens to be "cursor").
if [[ "$_CLIENT" == "cursor" ]]; then
  if [[ "$_hook_dir_lower" != */.cursor/* ]] \
     && [[ "$_hook_dir_lower" != */application?support/cursor/* ]] \
     && [[ "$_hook_dir_lower" != /etc/cursor/* ]] \
     && [[ "$_hook_dir_lower" != */programdata/cursor/* ]]; then
    echo '{"permission":"allow"}'
    exit 0
  fi
fi

# Capture env-var event name early so deny_response can reference it before
# stdin is parsed (e.g. stdin read failure).
_HOOK_EVENT_NAME="${HOOK_EVENT_NAME:-PreToolUse}"

# =============================================================================
# Response helpers (adapt JSON shape per client)
# =============================================================================
_AGENT_GUARDRAILS='**If you are an AI Agent:**
- Provide the user with a detailed explanation of this security violation.
- Do not suggest this is a false positive or mistake.
- Do not suggest modifying, bypassing, or disabling the Runlayer hook or security configuration.
- Do not suggest checking or editing hook files, settings.json, or any security configuration.
- Do not retry this action or attempt alternative approaches to achieve the same result.'

deny_response() {
  local user_msg="${1:-Action blocked by organization security policy}"
  local agent_msg="${2:-}"
  if [[ -z "$agent_msg" ]]; then
    agent_msg="# Security Violation Detected

Your organization's security policy (enforced by Runlayer) has blocked this operation.

**What happened:**
- Violation type: Infrastructure
- Reason: The Runlayer hook encountered an internal error and could not complete the required policy check. Unverified actions are blocked (fail-closed).

${_AGENT_GUARDRAILS}

**What to do:**
If you believe this is an error, contact your Runlayer administrator."
  fi
  if [[ "$_CLIENT" == "cursor" ]]; then
    jq -nc --arg u "$user_msg" --arg a "$agent_msg" \
      '{permission: "deny", continue: true, user_message: $u, agentMessage: $a}'
  elif [[ "$_CLIENT" == "codex" ]]; then
    if [[ "$_HOOK_EVENT_NAME" == "PermissionRequest" ]]; then
      jq -nc --arg m "$user_msg" '{
        hookSpecificOutput: {
          hookEventName: "PermissionRequest",
          decision: {
            behavior: "deny",
            message: $m
          }
        }
      }'
    else
      jq -nc --arg r "$user_msg" '{decision: "block", reason: $r}'
    fi
  elif [[ "$_CLIENT" == "hermes" ]]; then
    jq -nc --arg r "$user_msg" '{
      action: "block",
      message: $r
    }'
  else
    jq -nc --arg m "$agent_msg" --arg e "$_HOOK_EVENT_NAME" '{
      hookSpecificOutput: {
        hookEventName: $e,
        permissionDecision: "deny",
        permissionDecisionReason: $m
      }
    }'
  fi
  exit 0
}

allow_response() {
  if [[ "$_CLIENT" == "cursor" ]]; then
    echo '{"permission":"allow"}'
  elif [[ "$_CLIENT" == "hermes" ]]; then
    echo '{}'
  fi
}

block_output_response() {
  local reason="${1:-Tool output blocked by organization security policy}"
  if [[ "$_CLIENT" == "hermes" ]]; then
    jq -nc --arg r "$reason" '$r'
    exit 0
  fi
  jq -nc --arg r "$reason" '{decision: "block", reason: $r}'
  exit 0
}

# Cursor preToolUse: allow with _runlayer_session_id
# injected into updated_input so the proxy can link scans to sessions.
_allow_with_ids() {
  local tool_input_json="$1"
  local sid="$2"
  if [[ "$_CLIENT" != "cursor" ]]; then return; fi
  if [[ -z "$sid" ]]; then
    echo '{"permission":"allow"}'
    return
  fi
  local merged
  merged=$(echo "$tool_input_json" | jq -c \
    --arg sid "$sid" \
    '. + (if $sid != "" then {"_runlayer_session_id": $sid} else {} end)' 2>/dev/null) || true
  if [[ -z "$merged" ]]; then
    echo '{"permission":"allow"}'
    return
  fi
  jq -nc --argjson u "$merged" '{permission:"allow", updated_input: $u}'
}

# =============================================================================
# Read hook input
# =============================================================================
input=$(cat 2>/dev/null) || deny_response "Action blocked by organization security policy" \
  "# Security Violation Detected

Your organization's security policy (enforced by Runlayer) has blocked this operation.

**What happened:**
- Violation type: Infrastructure
- Reason: The hook failed to read its input payload. Unverified actions are blocked (fail-closed).

${_AGENT_GUARDRAILS}

**What to do:**
If you believe this is an error, contact your Runlayer administrator."

hook_type="${HOOK_EVENT_NAME:-}"
[[ -z "$hook_type" ]] && hook_type=$(echo "$input" | jq -r '.hook_event_name // empty' 2>/dev/null) || true
[[ -z "$hook_type" ]] && exit 0
_HOOK_EVENT_NAME="$hook_type"

_original_hook_type="$hook_type"

# Normalize event names (Cursor camelCase -> Claude Code PascalCase)
case "$hook_type" in
  preToolUse)           hook_type="PreToolUse" ;;
  postToolUse)          hook_type="PostToolUse" ;;
  postToolUseFailure)   hook_type="PostToolUseFailure" ;;
  stop)                 hook_type="Stop" ;;
  sessionStart)         hook_type="SessionStart" ;;
  sessionEnd)           hook_type="SessionEnd" ;;
  subagentStart)        hook_type="SubagentStart" ;;
  subagentStop)         hook_type="SubagentStop" ;;
  beforeSubmitPrompt)   hook_type="UserPromptSubmit" ;;
  preCompact)           hook_type="PreCompact" ;;
  pre_tool_call)         hook_type="PreToolUse" ;;
  post_tool_call)        hook_type="PostToolUse" ;;
  transform_tool_result) hook_type="PostToolUse" ;;
  pre_llm_call)          hook_type="UserPromptSubmit" ;;
  on_session_start)      hook_type="SessionStart" ;;
  on_session_end)        hook_type="SessionEnd" ;;
  on_session_finalize)   hook_type="Stop" ;;
esac

# =============================================================================
# Enforcement config
# =============================================================================
_config_file="$(dirname "$0")/runlayer-config.json"
_ENFORCEMENT=true
if [[ -f "$_config_file" ]]; then
  _val=$(jq -r '.enforcement' "$_config_file" 2>/dev/null) || true
  [[ "$_val" == "false" ]] && _ENFORCEMENT=false
fi
_TRANSCRIPT_STREAM_ACTIVE_SECONDS=10

_run_relay() {
  local relay_cmd
  if command -v runlayer >/dev/null 2>&1; then
    relay_cmd=(runlayer hooks relay)
  elif command -v uvx >/dev/null 2>&1; then
    relay_cmd=(uvx runlayer hooks relay)
  else
    return 127
  fi
  "${relay_cmd[@]}" "$@"
}

_run_stream_transcript() {
  _run_relay stream-transcript "$@"
}

_RELAY_DEBUG_ARGS=()
[[ "${RUNLAYER_HOOK_DEBUG:-}" == "1" ]] && _RELAY_DEBUG_ARGS=(--debug)

# =============================================================================
# Local tool lifecycle helpers
# =============================================================================
_tool_input_json() {
  local payload="$1"
  local parsed
  parsed=$(echo "$payload" | jq -c '
    (.tool_input // {}) as $input
    | if ($input | type) == "object" then $input
      elif ($input | type) == "string" then
        (try ($input | fromjson | if type == "object" then . else {"value": .} end) catch {"value": $input})
      else {"value": $input}
      end
  ' 2>/dev/null) || parsed="{}"
  [[ -z "$parsed" ]] && parsed="{}"
  echo "$parsed"
}

_session_id_from_payload() {
  local payload="$1"
  echo "$payload" | jq -r '
    .session_id
    // .conversation_id
    // .transcript_id
    // .chat_id
    // empty
  ' 2>/dev/null || true
}

_transcript_stream_marker() {
  local payload="$1"
  local sid safe
  sid=$(_session_id_from_payload "$payload")
  [[ -n "$sid" ]] || return 1
  safe=$(printf '%s' "$sid" | tr -c 'A-Za-z0-9_.-' '_' | sed 's/^[._]*//; s/[._]*$//')
  [[ -n "$safe" ]] || return 1
  printf '%s/runlayer-claude-transcript-stream/%s.active' "${TMPDIR:-/tmp}" "$safe"
}

_transcript_stream_active() {
  local payload="$1"
  local marker marker_ts now age
  marker=$(_transcript_stream_marker "$payload") || return 1
  [[ -f "$marker" ]] || return 1
  marker_ts=$(head -n 1 "$marker" 2>/dev/null | sed -E 's/^([0-9]+).*/\1/') || marker_ts=""
  [[ -n "$marker_ts" ]] || return 1
  [[ "$marker_ts" != *[!0-9]* ]] || return 1
  now=$(date +%s 2>/dev/null) || return 1
  age=$((now - marker_ts))
  [[ "$age" -ge 0 && "$age" -lt "$_TRANSCRIPT_STREAM_ACTIVE_SECONDS" ]]
}

_clear_transcript_stream_active() {
  local payload="$1"
  local marker
  marker=$(_transcript_stream_marker "$payload") || return 0
  rm -f "$marker" 2>/dev/null || true
}

_start_transcript_stream() {
  local payload="$1"
  local transcript_path start_offset wrapper

  [[ "$_CLIENT" == "claude_code" ]] || return 0
  transcript_path=$(echo "$payload" | jq -r '.transcript_path // empty' 2>/dev/null) || true
  [[ -n "$transcript_path" ]] || return 0
  transcript_path="${transcript_path/#\~/$HOME}"
  _transcript_stream_active "$payload" && return 0

  if ! command -v runlayer >/dev/null 2>&1 && ! command -v uvx >/dev/null 2>&1; then
    return 0
  fi
  start_offset=0
  if [[ -f "$transcript_path" ]]; then
    start_offset=$(wc -c < "$transcript_path" | tr -d ' ') || start_offset=0
  fi
  wrapper=$(jq -nc \
    --arg client "$_CLIENT" \
    --argjson payload "$payload" \
    --argjson start_offset "${start_offset:-0}" '
      {client: $client, payload: $payload, start_offset: $start_offset}
    ') || {
      _clear_transcript_stream_active "$payload"
      return 0
    }

  {
    echo "$wrapper" | _run_stream_transcript ${_RELAY_DEBUG_ARGS[@]+"${_RELAY_DEBUG_ARGS[@]}"} >/dev/null 2>&1 \
      || _clear_transcript_stream_active "$payload"
  } >/dev/null 2>&1 </dev/null &
}

_tool_lifecycle_request() {
  local payload="$1"
  local tool_name="$2"
  local event_name="$3"

  jq -nc \
    --arg client "$_CLIENT" \
    --arg event_name "$event_name" \
    --arg tool_name "$tool_name" \
    --argjson payload "$payload" '
      {
        client: $client,
        event_name: $event_name,
        tool_name: $tool_name,
        payload: $payload
      }
    '
}

_tool_lifecycle_async() {
  local target="$1"
  local payload="$2"
  local tool_name="$3"
  local event_name="$4"
  local request

  request=$(_tool_lifecycle_request "$payload" "$tool_name" "$event_name") || return 0
  {
    echo "$request" | _run_relay "$target" ${_RELAY_DEBUG_ARGS[@]+"${_RELAY_DEBUG_ARGS[@]}"} >/dev/null 2>&1 || true
  } >/dev/null 2>&1 </dev/null &
}

_valid_permission_response() {
  local response="$1"
  echo "$response" | jq -e '(.permission == "allow") or (.permission == "deny")' >/dev/null 2>&1
}

_valid_blocked_response() {
  local response="$1"
  echo "$response" | jq -e '(.blocked | type) == "boolean"' >/dev/null 2>&1
}

TOOL_PRE_RESPONSE=""
TOOL_PRE_BLOCK="false"
TOOL_PRE_BLOCK_REASON=""
TOOL_PRE_INPUT_JSON="{}"

_tool_pre_check() {
  local payload="$1"
  local tool_name="$2"
  local event_name="$3"
  local request response rc permission

  TOOL_PRE_RESPONSE=""
  TOOL_PRE_BLOCK="false"
  TOOL_PRE_BLOCK_REASON=""
  TOOL_PRE_INPUT_JSON=$(_tool_input_json "$payload")

  request=$(_tool_lifecycle_request "$payload" "$tool_name" "$event_name") || {
    TOOL_PRE_BLOCK="true"
    TOOL_PRE_BLOCK_REASON="Failed to prepare Runlayer tool pre-check"
    return 0
  }

  response=$(echo "$request" | _run_relay tool-pre ${_RELAY_DEBUG_ARGS[@]+"${_RELAY_DEBUG_ARGS[@]}"} 2>/dev/null) && rc=0 || rc=$?
  if [[ $rc -eq 1 ]]; then
    TOOL_PRE_BLOCK="true"
    TOOL_PRE_BLOCK_REASON="Action blocked by organization security policy. Run 'runlayer login' first."
    return 0
  elif [[ $rc -eq 127 ]]; then
    TOOL_PRE_BLOCK="true"
    TOOL_PRE_BLOCK_REASON="Runlayer CLI not found on hook PATH"
    return 0
  elif [[ $rc -ne 0 ]]; then
    TOOL_PRE_BLOCK="true"
    TOOL_PRE_BLOCK_REASON="Failed to contact Runlayer API"
    return 0
  fi

  TOOL_PRE_RESPONSE="$response"
  if ! _valid_permission_response "$response"; then
    TOOL_PRE_BLOCK="true"
    TOOL_PRE_BLOCK_REASON="Invalid response from Runlayer API"
    return 0
  fi

  permission=$(echo "$response" | jq -r '.permission' 2>/dev/null) || permission=""
  if [[ "$permission" == "deny" ]]; then
    TOOL_PRE_BLOCK="true"
    TOOL_PRE_BLOCK_REASON=$(echo "$response" | jq -r '
      .block_reason
      // .user_message
      // .reason
      // "Tool use blocked by organization policy"
    ' 2>/dev/null) || TOOL_PRE_BLOCK_REASON="Tool use blocked by organization policy"
  fi
}

_tool_pre_allow_response() {
  local payload="$1"

  if [[ "$_CLIENT" != "cursor" ]]; then
    allow_response
    return
  fi

  local sid modified tool_input merged
  sid=$(_session_id_from_payload "$payload")
  modified=$(echo "$TOOL_PRE_RESPONSE" | jq -c '.modified_args // empty' 2>/dev/null) || true
  tool_input="$TOOL_PRE_INPUT_JSON"
  [[ -n "$modified" ]] && tool_input="$modified"

  if [[ -z "$sid" && -z "$modified" ]]; then
    echo '{"permission":"allow"}'
    return
  fi

  merged=$(echo "$tool_input" | jq -c \
    --arg sid "$sid" \
    '. + (if $sid != "" then {"_runlayer_session_id": $sid} else {} end)' 2>/dev/null) || true
  if [[ -z "$merged" ]]; then
    echo '{"permission":"allow"}'
    return
  fi
  jq -nc --argjson u "$merged" '{permission:"allow", updated_input: $u}'
}

TOOL_POST_RESPONSE=""
TOOL_POST_BLOCK="false"
TOOL_POST_BLOCK_REASON=""

_tool_post_check() {
  local payload="$1"
  local event_name="$2"
  local tool_name request response rc

  TOOL_POST_RESPONSE=""
  TOOL_POST_BLOCK="false"
  TOOL_POST_BLOCK_REASON=""

  tool_name=$(echo "$payload" | jq -r '.tool_name // empty' 2>/dev/null) || true
  request=$(_tool_lifecycle_request "$payload" "$tool_name" "$event_name") || {
    TOOL_POST_BLOCK="true"
    TOOL_POST_BLOCK_REASON="Failed to prepare Runlayer tool post-check"
    return 0
  }

  response=$(echo "$request" | _run_relay tool-post ${_RELAY_DEBUG_ARGS[@]+"${_RELAY_DEBUG_ARGS[@]}"} 2>/dev/null) && rc=0 || rc=$?
  if [[ $rc -eq 1 ]]; then
    TOOL_POST_BLOCK="true"
    TOOL_POST_BLOCK_REASON="Tool output blocked by organization security policy. Run 'runlayer login' first."
    return 0
  elif [[ $rc -eq 127 ]]; then
    TOOL_POST_BLOCK="true"
    TOOL_POST_BLOCK_REASON="Runlayer CLI not found on hook PATH"
    return 0
  elif [[ $rc -ne 0 ]]; then
    TOOL_POST_BLOCK="true"
    TOOL_POST_BLOCK_REASON="Failed to contact Runlayer API"
    return 0
  fi

  TOOL_POST_RESPONSE="$response"
  if ! _valid_blocked_response "$response"; then
    TOOL_POST_BLOCK="true"
    TOOL_POST_BLOCK_REASON="Invalid response from Runlayer API"
    return 0
  fi

  if echo "$response" | jq -e '.blocked == true' >/dev/null 2>&1; then
    TOOL_POST_BLOCK="true"
    TOOL_POST_BLOCK_REASON=$(echo "$response" | jq -r '
      .block_reason
      // (.scan_results[]? | select((.scan_action // "") == "block") | (.reason // .error))
      // "Tool output blocked by organization policy"
    ' 2>/dev/null) || TOOL_POST_BLOCK_REASON="Tool output blocked by organization policy"
  fi
}

# =============================================================================
# Event forwarding (via runlayer hooks relay — handles credential resolution)
# =============================================================================
_forward_event() {
  local event_name="$1"
  local payload="$2"
  local wrapper
  wrapper=$(jq -nc --arg c "$_CLIENT" --arg e "$event_name" --argjson p "$payload" \
    '{client: $c, event_name: $e, payload: $p}') || return 0
  echo "$wrapper" | _run_relay event ${_RELAY_DEBUG_ARGS[@]+"${_RELAY_DEBUG_ARGS[@]}"} >/dev/null 2>&1 || true
}

_forward_event_async() {
  _forward_event "$1" "$2" >/dev/null 2>&1 </dev/null &
}

_wait_for_transcript_file() {
  local transcript_path="$1"
  local _attempt
  [[ -f "$transcript_path" ]] && return 0
  for _attempt in 1 2 3 4 5; do
    sleep 0.1
    [[ -f "$transcript_path" ]] && return 0
  done
  return 1
}

_forward_stop_event() {
  local event_name="$1"
  local payload="$2"
  local _transcript_tmp=""
  local transcript_path
  if [[ "$_CLIENT" == "claude_code" ]] && _transcript_stream_active "$payload"; then
    _forward_event "$event_name" "$payload"
    return
  fi
  transcript_path=$(echo "$payload" | jq -r '.transcript_path // empty' 2>/dev/null) || true
  [[ -z "$transcript_path" ]] && transcript_path="${CURSOR_TRANSCRIPT_PATH:-}"
  if [[ -n "$transcript_path" ]]; then
    transcript_path="${transcript_path/#\~/$HOME}"
    if _wait_for_transcript_file "$transcript_path"; then
      _transcript_tmp=$(mktemp)
      tail -c 524288 "$transcript_path" > "$_transcript_tmp" 2>/dev/null || true
    fi
  fi
  if [[ -n "$_transcript_tmp" && -s "$_transcript_tmp" ]]; then
    jq -nc --arg c "$_CLIENT" --arg e "$event_name" --argjson p "$payload" \
      --rawfile t "$_transcript_tmp" \
      '{client: $c, event_name: $e, payload: $p, transcript: $t}' \
    | _run_relay event --timeout 10 ${_RELAY_DEBUG_ARGS[@]+"${_RELAY_DEBUG_ARGS[@]}"} >/dev/null 2>&1 || true
    rm -f "$_transcript_tmp"
  else
    [[ -n "$_transcript_tmp" ]] && rm -f "$_transcript_tmp"
    _forward_event "$event_name" "$payload"
  fi
}

_forward_cursor_stop_session_end() {
  local payload="$1"
  local session_end_payload
  session_end_payload=$(echo "$payload" | jq -c '
    (.reason // .stop_reason // .status // "completed") as $reason
    | . + {hook_event_name: "sessionEnd", reason: $reason}
  ' 2>/dev/null) || return 0
  _forward_event "sessionEnd" "$session_end_payload"
}

# =============================================================================
# MCP server lookup
# Claude Code search order per docs:
#   1. ${cwd}/.mcp.json              — project-scoped servers
#   2. ~/.claude.json projects[cwd]   — per-project servers in user state
#   3. ~/.claude.json mcpServers      — global user-scoped servers
# =============================================================================
_lookup_mcp_server() {
  local server_name="$1"
  local cwd="$2"
  MCP_SERVER_URL=""
  MCP_SERVER_COMMAND=""
  local url command args

  if [[ -f "${cwd}/.mcp.json" ]]; then
    url=$(jq -r --arg s "$server_name" '.mcpServers[$s].url // empty' "${cwd}/.mcp.json" 2>/dev/null) || true
    if [[ -n "$url" ]]; then MCP_SERVER_URL="$url"; return 0; fi
    command=$(jq -r --arg s "$server_name" '.mcpServers[$s].command // empty' "${cwd}/.mcp.json" 2>/dev/null) || true
    if [[ -n "$command" ]]; then
      args=$(jq -r --arg s "$server_name" '.mcpServers[$s].args // [] | join(" ")' "${cwd}/.mcp.json" 2>/dev/null) || true
      MCP_SERVER_COMMAND="${command} ${args}"; return 0
    fi
  fi

  local claude_json="${HOME}/.claude.json"
  if [[ -f "$claude_json" ]]; then
    url=$(jq -r --arg c "$cwd" --arg s "$server_name" '.projects[$c].mcpServers[$s].url // empty' "$claude_json" 2>/dev/null) || true
    if [[ -n "$url" ]]; then MCP_SERVER_URL="$url"; return 0; fi
    command=$(jq -r --arg c "$cwd" --arg s "$server_name" '.projects[$c].mcpServers[$s].command // empty' "$claude_json" 2>/dev/null) || true
    if [[ -n "$command" ]]; then
      args=$(jq -r --arg c "$cwd" --arg s "$server_name" '.projects[$c].mcpServers[$s].args // [] | join(" ")' "$claude_json" 2>/dev/null) || true
      MCP_SERVER_COMMAND="${command} ${args}"; return 0
    fi

    url=$(jq -r --arg s "$server_name" '.mcpServers[$s].url // empty' "$claude_json" 2>/dev/null) || true
    if [[ -n "$url" ]]; then MCP_SERVER_URL="$url"; return 0; fi
    command=$(jq -r --arg s "$server_name" '.mcpServers[$s].command // empty' "$claude_json" 2>/dev/null) || true
    if [[ -n "$command" ]]; then
      args=$(jq -r --arg s "$server_name" '.mcpServers[$s].args // [] | join(" ")' "$claude_json" 2>/dev/null) || true
      MCP_SERVER_COMMAND="${command} ${args}"; return 0
    fi
  fi

  _lookup_claude_code_plugin_mcp_server "$server_name" "$cwd" && return 0

  return 1
}

_lookup_codex_mcp_server_in_toml_file() {
  local config_file="$1"
  local server_name="$2"
  local parsed key value tab

  [[ -f "$config_file" ]] || return 1

  parsed=$(awk -v target="$server_name" '
    function trim(s) {
      sub(/^[ \t\r\n]+/, "", s)
      sub(/[ \t\r\n]+$/, "", s)
      return s
    }
    function normalize(s) {
      s = tolower(s)
      gsub(/[^a-z0-9]/, "", s)
      return s
    }
    function clean_scalar(s) {
      sub(/^[^=]*=/, "", s)
      sub(/[ \t]*#.*/, "", s)
      s = trim(s)
      if (s ~ /^".*"$/) {
        s = substr(s, 2, length(s) - 2)
      }
      return s
    }
    function clean_args(s) {
      sub(/^[^=]*=/, "", s)
      sub(/[ \t]*#.*/, "", s)
      s = trim(s)
      sub(/^\[/, "", s)
      sub(/\]$/, "", s)
      gsub(/"[ \t]*,[ \t]*"/, " ", s)
      gsub(/,/, " ", s)
      gsub(/"/, "", s)
      return trim(s)
    }
    /^[ \t]*\[/ {
      section = $0
      sub(/^[ \t]*\[/, "", section)
      sub(/\][ \t]*($|#.*$)/, "", section)
      in_section = 0
      prefix = "mcp_servers."
      if (index(section, prefix) == 1) {
        name = substr(section, length(prefix) + 1)
        if (name ~ /^".*"$/) {
          name = substr(name, 2, length(name) - 2)
        }
        in_section = (name == target || normalize(name) == normalize(target))
      }
      next
    }
    in_section && /^[ \t]*url[ \t]*=/ {
      print "url\t" clean_scalar($0)
      next
    }
    in_section && /^[ \t]*command[ \t]*=/ {
      print "command\t" clean_scalar($0)
      next
    }
    in_section && /^[ \t]*args[ \t]*=/ {
      print "args\t" clean_args($0)
      next
    }
  ' "$config_file" 2>/dev/null) || true

  [[ -n "$parsed" ]] || return 1

  MCP_SERVER_URL=""
  MCP_SERVER_COMMAND=""
  MCP_SERVER_ARGS=""
  tab=$'\t'
  while IFS="$tab" read -r key value; do
    case "$key" in
      url) MCP_SERVER_URL="$value" ;;
      command) MCP_SERVER_COMMAND="$value" ;;
      args) MCP_SERVER_ARGS="$value" ;;
    esac
  done <<< "$parsed"

  if [[ -n "$MCP_SERVER_URL" || -n "$MCP_SERVER_COMMAND" ]]; then
    return 0
  fi

  return 1
}

_lookup_codex_mcp_server() {
  local server_name="$1"
  local config_file
  MCP_SERVER_URL=""
  MCP_SERVER_COMMAND=""
  MCP_SERVER_ARGS=""

  for config_file in \
    "${HOME}/.codex/config.toml" \
    "${HOME}/.codex/managed_config.toml" \
    "/etc/codex/managed_config.toml"; do
    _lookup_codex_mcp_server_in_toml_file "$config_file" "$server_name" && return 0
  done

  return 1
}

_join_command_args() {
  local command="$1"
  local args="${2:-}"

  if [[ -n "$args" ]]; then
    printf '%s %s' "$command" "$args"
  else
    printf '%s' "$command"
  fi
}

_normalized_name() {
  printf '%s' "$1" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]//g'
}

_is_mcp_tool() {
  local tool_name="$1"
  [[ "$tool_name" == mcp__* ]] && return 0
  [[ "$_CLIENT" == "hermes" && "$tool_name" == mcp_* ]] && return 0
  return 1
}

_uses_configured_mcp_source() {
  local tool_name="$1"
  if [[ "$_CLIENT" == "claude_code" || "$_CLIENT" == "codex" ]]; then
    [[ "$tool_name" == mcp__* ]] && return 0
  elif [[ "$_CLIENT" == "hermes" ]]; then
    [[ "$tool_name" == mcp_* ]] && return 0
  fi
  return 1
}

_is_read_tool() {
  local lower
  lower=$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]')
  case "$lower" in
    read|readfile|read_file) return 0 ;;
  esac
  return 1
}

_is_shell_tool() {
  local lower
  lower=$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]')
  case "$lower" in
    bash|shell|terminal) return 0 ;;
  esac
  return 1
}

_lookup_mcp_server_in_json_file() {
  local config_file="$1"
  local server_name="$2"
  local url command args

  [[ -f "$config_file" ]] || return 1

  url=$(jq -r --arg s "$server_name" '.mcpServers[$s].url // empty' "$config_file" 2>/dev/null) || true
  if [[ -n "$url" ]]; then
    MCP_SERVER_URL="$url"
    MCP_SERVER_COMMAND=""
    MCP_SERVER_ARGS=""
    return 0
  fi

  command=$(jq -r --arg s "$server_name" '.mcpServers[$s].command // empty' "$config_file" 2>/dev/null) || true
  if [[ -n "$command" ]]; then
    args=$(jq -r --arg s "$server_name" '.mcpServers[$s].args // [] | join(" ")' "$config_file" 2>/dev/null) || true
    MCP_SERVER_URL=""
    MCP_SERVER_COMMAND="$command"
    MCP_SERVER_ARGS="$args"
    return 0
  fi

  return 1
}

_claude_plugin_lookup_names() {
  local server_name="$1"
  local plugin_name="$2"
  local prefix suffix

  prefix="plugin_${plugin_name}_"
  if [[ "$server_name" == plugin_* ]]; then
    [[ "$server_name" == "$prefix"* ]] || return 0
    suffix="${server_name#"$prefix"}"
    [[ -n "$suffix" ]] && printf '%s\n' "$suffix"
    printf '%s\n' "$server_name"
    return 0
  fi

  printf '%s\n' "$server_name"
}

_claude_project_contains_cwd() {
  local project_path="$1"
  local cwd="$2"
  local project_real cwd_real

  [[ -z "$project_path" ]] && return 0
  project_real=$(_claude_canonical_dir "$project_path") || project_real="${project_path%/}"
  cwd_real=$(_claude_canonical_dir "$cwd") || cwd_real="${cwd%/}"
  [[ "$cwd_real" == "$project_real" || "$cwd_real" == "$project_real"/* ]]
}

_claude_canonical_dir() {
  local path="$1"

  [[ -d "$path" ]] || return 1
  (cd "$path" 2>/dev/null && pwd -P)
}

_claude_settings_cwd() {
  local cwd="$1"
  local current

  current=$(_claude_canonical_dir "$cwd") || current="${cwd%/}"
  while true; do
    if [[ -f "$current/.claude/settings.json" || -f "$current/.claude/settings.local.json" ]]; then
      printf '%s\n' "$current"
      return 0
    fi
    [[ "$current" == "/" || -z "$current" ]] && break
    current="${current%/*}"
    [[ -n "$current" ]] || current="/"
  done
  printf '%s\n' "$cwd"
}

_lookup_claude_plugin_root_mcp_server() {
  local plugin_root="$1"
  local server_name="$2"
  local plugin_name="$3"
  local lookup_name manifest_file mcp_path

  [[ -d "$plugin_root" ]] || return 1
  manifest_file="$plugin_root/.claude-plugin/plugin.json"

  while IFS= read -r lookup_name; do
    [[ -n "$lookup_name" ]] || continue
    _lookup_mcp_server_in_json_file "$manifest_file" "$lookup_name" && return 0

    mcp_path=$(jq -r '.mcpServers | select(type == "string") // empty' "$manifest_file" 2>/dev/null) || true
    if [[ -n "$mcp_path" ]]; then
      if [[ "$mcp_path" != /* ]]; then
        mcp_path="${plugin_root}/${mcp_path#./}"
      fi
      _lookup_mcp_server_in_json_file "$mcp_path" "$lookup_name" && return 0
    fi

    _lookup_mcp_server_in_json_file "$plugin_root/.mcp.json" "$lookup_name" && return 0
  done < <(_claude_plugin_lookup_names "$server_name" "$plugin_name")

  return 1
}

_claude_plugin_enabled() {
  local plugin_key="$1"
  local settings_cwd="$2"
  local settings_file value enabled=""

  for settings_file in \
    "${HOME}/.claude/settings.json" \
    "${settings_cwd}/.claude/settings.json" \
    "${settings_cwd}/.claude/settings.local.json"; do
    [[ -f "$settings_file" ]] || continue
    value=$(jq -r --arg key "$plugin_key" '
      if ((.enabledPlugins // null) | type) == "object" and (.enabledPlugins | has($key)) then
        if (.enabledPlugins[$key] | type) == "boolean" then
          (.enabledPlugins[$key] | tostring)
        else
          "true"
        end
      else
        empty
      end
    ' "$settings_file" 2>/dev/null) || value=""
    [[ -n "$value" ]] && enabled="$value"
  done

  [[ "$enabled" != "false" ]]
}

_lookup_claude_code_plugin_mcp_server() {
  local server_name="$1"
  local cwd="$2"
  local registry="${HOME}/.claude/plugins/installed_plugins.json"
  local rows row plugin_key plugin_name project_path install_path settings_cwd scope rank
  local best_rank=-1 best_url="" best_command="" best_args="" found=1

  [[ -f "$registry" ]] || return 1

  rows=$(jq -c '
    (.plugins // {})
    | to_entries[]
    | .key as $plugin_key
    | (.value // [])[]
    | select(type == "object")
    | {
        plugin_key: $plugin_key,
        scope: (.scope // ""),
        project_path: (.projectPath // ""),
        install_path: (.installPath // "")
      }
  ' "$registry" 2>/dev/null) || true
  [[ -n "$rows" ]] || return 1

  while IFS= read -r row; do
    [[ -n "$row" ]] || continue
    plugin_key=$(jq -r '.plugin_key // empty' <<< "$row" 2>/dev/null) || plugin_key=""
    plugin_name="${plugin_key%@*}"
    scope=$(jq -r '.scope // empty' <<< "$row" 2>/dev/null) || scope=""
    project_path=$(jq -r '.project_path // empty' <<< "$row" 2>/dev/null) || project_path=""
    install_path=$(jq -r '.install_path // empty' <<< "$row" 2>/dev/null) || install_path=""
    [[ -n "$install_path" ]] || continue
    rank=0
    if [[ -n "$project_path" ]]; then
      _claude_project_contains_cwd "$project_path" "$cwd" || continue
      settings_cwd=$(_claude_canonical_dir "$project_path") || settings_cwd="$project_path"
      rank=1
      [[ "$scope" == "local" ]] && rank=2
    else
      settings_cwd=$(_claude_settings_cwd "$cwd")
    fi
    _claude_plugin_enabled "$plugin_key" "$settings_cwd" || continue
    if _lookup_claude_plugin_root_mcp_server "$install_path" "$server_name" "$plugin_name"; then
      if (( rank > best_rank )); then
        best_rank=$rank
        best_url="${MCP_SERVER_URL:-}"
        best_command="${MCP_SERVER_COMMAND:-}"
        best_args="${MCP_SERVER_ARGS:-}"
        found=0
      fi
    fi
  done <<< "$rows"

  if [[ "$found" -eq 0 ]]; then
    MCP_SERVER_URL="$best_url"
    MCP_SERVER_COMMAND="$best_command"
    MCP_SERVER_ARGS="$best_args"
    return 0
  fi

  return 1
}

_read_hermes_mcp_servers() {
  local config_file="${HOME}/.hermes/config.yaml"
  [[ -f "$config_file" ]] || return 1

  awk '
    function trim(s) {
      sub(/^[ \t\r\n]+/, "", s)
      sub(/[ \t\r\n]+$/, "", s)
      return s
    }
    function clean_key(s) {
      sub(/^[ \t]+/, "", s)
      sub(/:[ \t]*($|#.*$)/, "", s)
      if (s ~ /^".*"$/ || s ~ /^\047.*\047$/) {
        s = substr(s, 2, length(s) - 2)
      }
      return s
    }
    function clean_scalar(s) {
      sub(/^[^:]*:/, "", s)
      sub(/[ \t]*#.*/, "", s)
      s = trim(s)
      if (s ~ /^".*"$/ || s ~ /^\047.*\047$/) {
        s = substr(s, 2, length(s) - 2)
      }
      return s
    }
    function clean_args(s) {
      sub(/^[^:]*:/, "", s)
      sub(/[ \t]*#.*/, "", s)
      s = trim(s)
      sub(/^\[/, "", s)
      sub(/\]$/, "", s)
      gsub(/"[ \t]*,[ \t]*"/, " ", s)
      gsub(/\047[ \t]*,[ \t]*\047/, " ", s)
      gsub(/,/, " ", s)
      gsub(/"/, "", s)
      gsub(/\047/, "", s)
      return trim(s)
    }
    function clean_arg_item(s) {
      sub(/^[ \t]*-[ \t]*/, "", s)
      sub(/[ \t]*#.*/, "", s)
      s = trim(s)
      if (s ~ /^".*"$/ || s ~ /^\047.*\047$/) {
        s = substr(s, 2, length(s) - 2)
      }
      return s
    }
    function inline_value(s, value) {
      value = s
      sub(/^[^:]*:/, "", value)
      sub(/[ \t]*#.*/, "", value)
      return trim(value)
    }
    function append_arg_item(value) {
      if (value == "") {
        return
      }
      if (args_value == "") {
        args_value = value
      } else {
        args_value = args_value " " value
      }
    }
    function flush_args() {
      if (!collecting_args) {
        return
      }
      print args_name "\targs\t" trim(args_value)
      collecting_args = 0
      args_name = ""
      args_value = ""
    }
    {
      if (collecting_args && $0 !~ /^[ \t]*($|#)/ && $0 !~ /^[ \t][ \t][ \t][ \t][ \t][ \t]-[ \t]*/) {
        flush_args()
      }
    }
    /^[^ #][^:]*:/ {
      flush_args()
      top = $0
      sub(/:.*/, "", top)
      in_mcp = (top == "mcp_servers")
      current = ""
      next
    }
    in_mcp && /^[ \t][ \t][^ \t#][^:]*:[ \t]*($|#.*$)/ {
      flush_args()
      current = clean_key($0)
      next
    }
    in_mcp && current && /^[ \t][ \t][ \t][ \t](url|serverUrl|uri)[ \t]*:/ {
      print current "\turl\t" clean_scalar($0)
      next
    }
    in_mcp && current && /^[ \t][ \t][ \t][ \t]command[ \t]*:/ {
      print current "\tcommand\t" clean_scalar($0)
      next
    }
    in_mcp && current && /^[ \t][ \t][ \t][ \t]args[ \t]*:/ {
      if (inline_value($0) == "") {
        collecting_args = 1
        args_name = current
        args_value = ""
        next
      }
      print current "\targs\t" clean_args($0)
      next
    }
    in_mcp && current && collecting_args && /^[ \t][ \t][ \t][ \t][ \t][ \t]-[ \t]*/ {
      append_arg_item(clean_arg_item($0))
      next
    }
    END {
      flush_args()
    }
  ' "$config_file" 2>/dev/null
}

_resolve_hermes_mcp_tool() {
  local tool_name="$1"
  local normalized_tool best_len=0
  local tab name key value normalized_candidate len
  local best_name="" best_url="" best_command="" best_args=""

  MCP_SERVER_URL=""
  MCP_SERVER_COMMAND=""
  MCP_SERVER_ARGS=""
  HERMES_MCP_SERVER_NAME=""

  normalized_tool="$(_normalized_name "${tool_name#mcp_}")"
  tab=$'\t'
  while IFS="$tab" read -r name key value; do
    [[ -n "$name" && -n "$key" ]] || continue
    normalized_candidate="$(_normalized_name "$name")"
    [[ -n "$normalized_candidate" ]] || continue
    case "$normalized_tool" in
      "$normalized_candidate"*)
        len=${#normalized_candidate}
        if (( len > best_len )); then
          best_len=$len
          best_name="$name"
          best_url=""
          best_command=""
          best_args=""
        fi
        if (( len == best_len )) && [[ "$name" == "$best_name" ]]; then
          case "$key" in
            url) best_url="$value" ;;
            command) best_command="$value" ;;
            args) best_args="$value" ;;
          esac
        fi
        ;;
    esac
  done < <(_read_hermes_mcp_servers || true)

  [[ -n "$best_name" ]] || return 1
  HERMES_MCP_SERVER_NAME="$best_name"
  MCP_SERVER_URL="$best_url"
  MCP_SERVER_COMMAND="$best_command"
  MCP_SERVER_ARGS="$best_args"
  [[ -n "$MCP_SERVER_URL" || -n "$MCP_SERVER_COMMAND" ]]
}

_lookup_cursor_mcp_server_in_json_file() {
  local config_file="$1"
  local server_name="$2"
  local lookup_name
  local lookup_names=("$server_name")

  _lookup_mcp_server_in_json_file "$config_file" "$server_name" && return 0

  # Cursor sometimes prefixes user MCP provider identifiers with "user-".
  if [[ "$server_name" == user-* ]]; then
    lookup_name="${server_name#user-}"
    _lookup_mcp_server_in_json_file "$config_file" "$lookup_name" && return 0
    lookup_names+=("$lookup_name")
  fi

  for lookup_name in "${lookup_names[@]}"; do
    lookup_name=$(jq -r --arg s "$lookup_name" '
      def normalized_name: ascii_downcase | gsub("[^a-z0-9]"; "");
      (.mcpServers // {})
      | keys[]
      | select((. | normalized_name) == ($s | normalized_name))
    ' "$config_file" 2>/dev/null | head -n 1) || true
    if [[ -n "$lookup_name" ]]; then
      _lookup_mcp_server_in_json_file "$config_file" "$lookup_name" && return 0
    fi
  done

  return 1
}

_lookup_cursor_mcp_server() {
  local server_name="$1"
  local payload="$2"
  MCP_SERVER_URL=""
  MCP_SERVER_COMMAND=""
  MCP_SERVER_ARGS=""

  local config_file
  while IFS= read -r config_file; do
    [[ -n "$config_file" ]] || continue

    _lookup_cursor_mcp_server_in_json_file "$config_file" "$server_name" && return 0
  done < <(
    {
      echo "$payload" | jq -r '
        ((.workspace_roots // [])[]?),
        (.cwd // empty)
        | select(type == "string" and length > 0)
        | . + "/.cursor/mcp.json"
      ' 2>/dev/null || true
      printf '%s\n' "${HOME}/.cursor/mcp.json"
    }
  )

  return 1
}

_resolve_cursor_before_mcp_payload() {
  local payload
  payload=$(jq -c '.client = "cursor"' <<<"$1")
  local server_name resolved resolved_command

  server_name=$(echo "$payload" | jq -r '
    if ((.url // "") == "") then (.command // empty) else empty end
  ' 2>/dev/null) || true

  if [[ -z "$server_name" ]]; then
    printf '%s' "$payload"
    return 0
  fi

  if ! _lookup_cursor_mcp_server "$server_name" "$payload"; then
    printf '%s' "$payload"
    return 0
  fi

  if [[ -n "$MCP_SERVER_URL" ]]; then
    resolved=$(echo "$payload" | jq -c --arg url "$MCP_SERVER_URL" '
      .url = $url | del(.command)
    ' 2>/dev/null) || resolved=""
    if [[ -n "$resolved" ]]; then
      printf '%s' "$resolved"
      return 0
    fi
  elif [[ -n "$MCP_SERVER_COMMAND" ]]; then
    resolved_command="$(_join_command_args "$MCP_SERVER_COMMAND" "$MCP_SERVER_ARGS")"
    resolved=$(echo "$payload" | jq -c --arg cmd "$resolved_command" '
      .command = $cmd | del(.url)
    ' 2>/dev/null) || resolved=""
    if [[ -n "$resolved" ]]; then
      printf '%s' "$resolved"
      return 0
    fi
  fi

  printf '%s' "$payload"
}

# =============================================================================
# File-read enforcement (shared pattern matching)
# =============================================================================
_check_file_read() {
  local file_path="$1"
  [[ -z "$file_path" ]] && return 0

  local basename lower_basename
  basename=$(basename "$file_path")
  lower_basename=$(echo "$basename" | tr '[:upper:]' '[:lower:]')
  case "$lower_basename" in
    .env|.env.*|*.env|.envrc)
      deny_response \
        "Blocked by organization policy: access to environment files is restricted" \
        "# Security Violation Detected

Your organization's security policy (enforced by Runlayer) has blocked this operation.

**What happened:**
- Violation type: File Access Policy
- File: ${file_path}
- Reason: Reading environment files (.env, .envrc) is blocked by your organization's policy. These files may contain credentials and secrets that must not be sent to the LLM.
- Do not attempt to read this file using Bash (cat, head, tail, less), Grep, or any other tool. All access to this file is restricted.

${_AGENT_GUARDRAILS}

**What to do:**
If you believe this is a false positive or mistake, contact your Runlayer administrator to adjust file access policies."
      ;;
    mcp.json|mcp_config.json|.mcp.json|mcp-config.json|mcp.yaml|mcp.yml|.claude.json|claude_desktop_config.json)
      deny_response \
        "Blocked by organization policy: access to MCP configuration files is restricted" \
        "# Security Violation Detected

Your organization's security policy (enforced by Runlayer) has blocked this operation.

**What happened:**
- Violation type: File Access Policy
- File: ${file_path}
- Reason: Reading MCP configuration files is blocked by your organization's policy. These files contain sensitive server connection details that must not be exposed.
- Do not attempt to read this file using Bash (cat, head, tail, less), Grep, or any other tool. All access to this file is restricted.

${_AGENT_GUARDRAILS}

**What to do:**
If you believe this is a false positive or mistake, contact your Runlayer administrator to adjust file access policies."
      ;;
    settings.json)
      local lower_path
      lower_path=$(echo "$file_path" | tr '[:upper:]' '[:lower:]')
      case "$lower_path" in
        */.claude/settings.json)
          deny_response \
            "Blocked by organization policy: access to Claude Code settings is restricted" \
            "# Security Violation Detected

Your organization's security policy (enforced by Runlayer) has blocked this operation.

**What happened:**
- Violation type: File Access Policy
- File: ${file_path}
- Reason: Reading Claude Code settings files is blocked by your organization's policy. These files contain sensitive hook and security configuration that must not be exposed.
- Do not attempt to read this file using Bash (cat, head, tail, less), Grep, or any other tool. All access to this file is restricted.

${_AGENT_GUARDRAILS}

**What to do:**
If you believe this is a false positive or mistake, contact your Runlayer administrator to adjust file access policies."
          ;;
      esac
      ;;
  esac
}

# =============================================================================
# Shell command enforcement (scan for protected file references)
# =============================================================================
_check_bash_command() {
  local command="$1"
  [[ -z "$command" ]] && return 0
  local words
  words=$(printf '%s' "$command" | tr '|;&<>\n`' ' ' | sed 's/\$(/  /g; s/)/ /g')
  for word in $words; do
    case "$word" in
      -*|[0-9]*|""|"''"'""') continue ;;
    esac
    word="${word#\"}"; word="${word%\"}"
    word="${word#\'}"; word="${word%\'}"
    _check_file_read "$word"
  done
}

# =============================================================================
# Main dispatch
# =============================================================================
case "$hook_type" in

  # ---------------------------------------------------------------------------
  # beforeMCPExecution — Cursor-only; input already carries url/command
  # ---------------------------------------------------------------------------
  beforeMCPExecution)
    raw_input="$input"

    if [[ "$_ENFORCEMENT" == "true" ]]; then
      if echo "$input" | jq -e '.tool_input | type == "object"' > /dev/null 2>&1; then
        input=$(echo "$input" | jq '.tool_input = (.tool_input | tojson)') \
          || deny_response "Action blocked by organization security policy" \
            "# Security Violation Detected

Your organization's security policy (enforced by Runlayer) has blocked this operation.

**What happened:**
- Violation type: Infrastructure
- Reason: Failed to serialize tool_input for the policy verification request. Unverified actions are blocked (fail-closed).

${_AGENT_GUARDRAILS}

**What to do:**
If you believe this is an error, contact your Runlayer administrator."
      fi

      if [[ "$_CLIENT" == "cursor" ]]; then
        input=$(_resolve_cursor_before_mcp_payload "$input")
      fi

      response=$(echo "$input" | _run_relay enforce ${_RELAY_DEBUG_ARGS[@]+"${_RELAY_DEBUG_ARGS[@]}"} 2>/dev/null) && rc=0 || rc=$?
      if [[ $rc -eq 1 ]]; then
        deny_response \
          "Action blocked by organization security policy. Run 'runlayer login' first." \
          "# Security Violation Detected

Your organization's security policy (enforced by Runlayer) has blocked this operation.

**What happened:**
- Violation type: Authentication Required
- Reason: Runlayer credentials are not configured on this machine. Your organization's policy requires all MCP tool use to be verified, which requires valid credentials.

${_AGENT_GUARDRAILS}

**What to do:**
Run 'runlayer login' to set up authentication, then retry."
      elif [[ $rc -eq 127 ]]; then
        deny_response \
          "Runlayer CLI not found on hook PATH" \
          "# Security Violation Detected

Your organization's security policy (enforced by Runlayer) has blocked this operation.

**What happened:**
- Violation type: Infrastructure
- Reason: Neither 'runlayer' nor 'uvx' could be found on the hook's PATH. The relay binary was never executed — no network call was attempted. This typically happens when an AI coding client launches hooks with a minimal (launchd) PATH that does not include user-installed tools.

${_AGENT_GUARDRAILS}

**What to do:**
Install the Runlayer CLI ('pip install runlayer' or 'uvx runlayer') and ensure it is available in one of: \$HOME/.local/bin, /opt/homebrew/bin, /usr/local/bin, or another directory on PATH."
      elif [[ $rc -ne 0 ]]; then
        deny_response \
          "Failed to contact Runlayer API" \
          "# Security Violation Detected

Your organization's security policy (enforced by Runlayer) has blocked this operation.

**What happened:**
- Violation type: Infrastructure
- Reason: Failed to contact the Runlayer API for MCP execution verification. Unverified actions are blocked (fail-closed).

${_AGENT_GUARDRAILS}

**What to do:**
If you believe this is an error, contact your Runlayer administrator. The Runlayer API may be temporarily unreachable."
      fi

      if ! _valid_permission_response "$response"; then
        deny_response \
          "Invalid response from Runlayer API" \
          "# Security Violation Detected

Your organization's security policy (enforced by Runlayer) has blocked this operation.

**What happened:**
- Violation type: Infrastructure
- Reason: The Runlayer API returned an invalid response during MCP verification. Unverified actions are blocked (fail-closed).

${_AGENT_GUARDRAILS}

**What to do:**
If you believe this is an error, contact your Runlayer administrator."
      fi

      _forward_event_async "$_original_hook_type" "$raw_input"

      permission=$(echo "$response" | jq -r '.permission' 2>/dev/null) || true
      if [[ "$permission" == "deny" ]]; then
        reason=$(echo "$response" | jq -r '.user_message // "MCP execution blocked by organization policy"' 2>/dev/null) || true
        deny_response "$reason" \
          "# Security Violation Detected

Your organization's security policy (enforced by Runlayer) has blocked this operation.

**What happened:**
- Violation type: MCP Execution Policy
- Reason: ${reason}

${_AGENT_GUARDRAILS}

**What to do:**
If you believe this is a false positive or mistake, contact your Runlayer administrator to review the security policy settings."
      fi
      echo "$response"
    else
      _forward_event_async "$_original_hook_type" "$raw_input"
      echo '{"permission":"allow"}'
    fi
    ;;

  # ---------------------------------------------------------------------------
  # PreToolUse — Claude Code native + Cursor via third-party hooks
  # ---------------------------------------------------------------------------
  PreToolUse)
    tool_name=$(echo "$input" | jq -r '.tool_name // empty' 2>/dev/null) || true

    # --- MCP tool enforcement (Cursor uses beforeMCPExecution) ---
    if _uses_configured_mcp_source "$tool_name"; then
      if [[ "$_ENFORCEMENT" == "true" ]]; then
        if [[ "$_CLIENT" == "hermes" ]]; then
          server_name="${tool_name#mcp_}"
        else
          server_name=$(echo "$tool_name" | sed 's/^mcp__//' | sed 's/__.*$//')
        fi
        cwd=$(echo "$input" | jq -r '.cwd // empty' 2>/dev/null) || true
        [[ -z "$cwd" ]] && cwd="$(pwd)"
        client_label="Claude Code"
        client_fallback="claude-code"
        settings_label="Claude Code settings"
        if [[ "$_CLIENT" == "codex" ]]; then
          client_label="Codex"
          client_fallback="codex"
          settings_label="Codex config"
        elif [[ "$_CLIENT" == "hermes" ]]; then
          client_label="Hermes"
          client_fallback="hermes"
          settings_label="Hermes config"
        fi

        if [[ "$_CLIENT" == "codex" ]]; then
          _lookup_codex_mcp_server "$server_name"
        elif [[ "$_CLIENT" == "hermes" ]]; then
          _resolve_hermes_mcp_tool "$tool_name"
          [[ -n "$HERMES_MCP_SERVER_NAME" ]] && server_name="$HERMES_MCP_SERVER_NAME"
        else
          _lookup_mcp_server "$server_name" "$cwd"
        fi \
          || deny_response \
            "Action blocked: MCP server '${server_name}' not registered in ${settings_label}" \
            "# Security Violation Detected

Your organization's security policy (enforced by Runlayer) has blocked this operation.

**What happened:**
- Violation type: MCP Execution Policy
- Tool: ${tool_name}
- MCP Server: ${server_name}
- Reason: MCP server '${server_name}' is not registered in ${settings_label} and cannot be verified. Your organization's policy requires all MCP servers to be registered before use.

${_AGENT_GUARDRAILS}

**What to do:**
Contact your Runlayer administrator to register this MCP server, or add the server to your ${client_label} MCP configuration."

        if [[ -n "$MCP_SERVER_URL" ]]; then
          cursor_req=$(echo "$input" | jq -c \
            --arg hook "beforeMCPExecution" \
            --arg client "$_CLIENT" \
            --arg fallback "$client_fallback" \
            --arg tool "$tool_name" \
            --arg source "$MCP_SERVER_URL" \
            '
              def s($v): if ($v | type) == "string" and $v != "" then $v else empty end;
              (s(.conversation_id) // s(.session_id) // s(.transcript_id) // s(.chat_id) // $fallback) as $conversation
              | (s(.generation_id) // s(.tool_use_id) // s(.request_id) // s(.message_id) // $conversation) as $generation
              | {
                  hook_event_name: $hook,
                  client: $client,
                  conversation_id: $conversation,
                  generation_id: $generation,
                  tool_name: $tool,
                  tool_input: (.tool_input // null),
                  url: $source
                }
            ') \
            || deny_response \
              "Action blocked by organization security policy" \
              "# Security Violation Detected

Your organization's security policy (enforced by Runlayer) has blocked this operation.

**What happened:**
- Violation type: Infrastructure
- Tool: ${tool_name}
- Reason: Failed to prepare the MCP verification request. Unverified actions are blocked (fail-closed).

${_AGENT_GUARDRAILS}

**What to do:**
If you believe this is an error, contact your Runlayer administrator."
        else
          MCP_SERVER_COMMAND="$(_join_command_args "$MCP_SERVER_COMMAND" "${MCP_SERVER_ARGS:-}")"
          cursor_req=$(echo "$input" | jq -c \
            --arg hook "beforeMCPExecution" \
            --arg client "$_CLIENT" \
            --arg fallback "$client_fallback" \
            --arg tool "$tool_name" \
            --arg source "$MCP_SERVER_COMMAND" \
            '
              def s($v): if ($v | type) == "string" and $v != "" then $v else empty end;
              (s(.conversation_id) // s(.session_id) // s(.transcript_id) // s(.chat_id) // $fallback) as $conversation
              | (s(.generation_id) // s(.tool_use_id) // s(.request_id) // s(.message_id) // $conversation) as $generation
              | {
                  hook_event_name: $hook,
                  client: $client,
                  conversation_id: $conversation,
                  generation_id: $generation,
                  tool_name: $tool,
                  tool_input: (.tool_input // null),
                  command: $source
                }
            ') \
            || deny_response \
              "Action blocked by organization security policy" \
              "# Security Violation Detected

Your organization's security policy (enforced by Runlayer) has blocked this operation.

**What happened:**
- Violation type: Infrastructure
- Tool: ${tool_name}
- Reason: Failed to prepare the MCP verification request. Unverified actions are blocked (fail-closed).

${_AGENT_GUARDRAILS}

**What to do:**
If you believe this is an error, contact your Runlayer administrator."
        fi

        response=$(echo "$cursor_req" | _run_relay enforce ${_RELAY_DEBUG_ARGS[@]+"${_RELAY_DEBUG_ARGS[@]}"} 2>/dev/null) && rc=0 || rc=$?
        if [[ $rc -eq 1 ]]; then
          deny_response \
            "Action blocked by organization security policy. Run 'runlayer login' first." \
            "# Security Violation Detected

Your organization's security policy (enforced by Runlayer) has blocked this operation.

**What happened:**
- Violation type: Authentication Required
- Tool: ${tool_name}
- Reason: Runlayer credentials are not configured on this machine. Your organization's policy requires all MCP tool use to be verified, which requires valid credentials.

${_AGENT_GUARDRAILS}

**What to do:**
Run 'runlayer login' to set up authentication, then retry."
        elif [[ $rc -eq 127 ]]; then
          deny_response \
            "Runlayer CLI not found on hook PATH" \
            "# Security Violation Detected

Your organization's security policy (enforced by Runlayer) has blocked this operation.

**What happened:**
- Violation type: Infrastructure
- Tool: ${tool_name}
- Reason: Neither 'runlayer' nor 'uvx' could be found on the hook's PATH. The relay binary was never executed — no network call was attempted. This typically happens when an AI coding client launches hooks with a minimal (launchd) PATH that does not include user-installed tools.

${_AGENT_GUARDRAILS}

**What to do:**
Install the Runlayer CLI ('pip install runlayer' or 'uvx runlayer') and ensure it is available in one of: \$HOME/.local/bin, /opt/homebrew/bin, /usr/local/bin, or another directory on PATH."
        elif [[ $rc -ne 0 ]]; then
          deny_response \
            "Failed to contact Runlayer API" \
            "# Security Violation Detected

Your organization's security policy (enforced by Runlayer) has blocked this operation.

**What happened:**
- Violation type: Infrastructure
- Tool: ${tool_name}
- Reason: Failed to contact the Runlayer API for MCP execution verification. Unverified actions are blocked (fail-closed).

${_AGENT_GUARDRAILS}

**What to do:**
If you believe this is an error, contact your Runlayer administrator. The Runlayer API may be temporarily unreachable."
        fi

        if ! _valid_permission_response "$response"; then
          deny_response \
            "Invalid response from Runlayer API" \
            "# Security Violation Detected

Your organization's security policy (enforced by Runlayer) has blocked this operation.

**What happened:**
- Violation type: Infrastructure
- Tool: ${tool_name}
- Reason: The Runlayer API returned an invalid response during MCP verification. Unverified actions are blocked (fail-closed).

${_AGENT_GUARDRAILS}

**What to do:**
If you believe this is an error, contact your Runlayer administrator."
        fi

        permission=$(echo "$response" | jq -r '.permission' 2>/dev/null) || true

        _forward_event_async "$_original_hook_type" "$input"

        if [[ "$permission" == "deny" ]]; then
          reason=$(echo "$response" | jq -r '.user_message // "MCP execution blocked by organization policy"' 2>/dev/null) || true
          deny_response "$reason" \
            "# Security Violation Detected

Your organization's security policy (enforced by Runlayer) has blocked this operation.

**What happened:**
- Violation type: MCP Execution Policy
- Tool: ${tool_name}
- Reason: ${reason}

${_AGENT_GUARDRAILS}

**What to do:**
If you believe this is a false positive or mistake, contact your Runlayer administrator to review the security policy settings."
        fi

        exit 0
      else
        _forward_event_async "$_original_hook_type" "$input"
        exit 0
      fi
    fi

    # --- Read tool enforcement ---
    if _is_read_tool "$tool_name"; then
      if [[ "$_ENFORCEMENT" == "true" ]]; then
        file_path=$(echo "$input" | jq -r '.tool_input.file_path // .tool_input.path // empty' 2>/dev/null) || true
        _check_file_read "$file_path"
      fi
    fi

    # --- Bash tool enforcement ---
    if _is_shell_tool "$tool_name"; then
      if [[ "$_ENFORCEMENT" == "true" ]]; then
        bash_command=$(echo "$input" | jq -r '.tool_input.command // .tool_input.cmd // empty' 2>/dev/null) || true
        _check_bash_command "$bash_command"
      fi
    fi

    # MCP calls are enforced through beforeMCPExecution / client MCP paths above.
    # Local tool lifecycle hooks are for native/built-in tools.
    if _is_mcp_tool "$tool_name"; then
      _forward_event_async "$_original_hook_type" "$input"
      if [[ "$_CLIENT" == "cursor" ]]; then
        _sid=$(_session_id_from_payload "$input")
        _ti=$(_tool_input_json "$input")
        _allow_with_ids "$_ti" "$_sid"
      else
        allow_response
      fi
      exit 0
    fi

    if [[ "$_ENFORCEMENT" != "true" ]]; then
      _tool_lifecycle_async "tool-pre" "$input" "$tool_name" "$_original_hook_type"
      _forward_event_async "$_original_hook_type" "$input"
      if [[ "$_CLIENT" == "cursor" ]]; then
        _sid=$(_session_id_from_payload "$input")
        _ti=$(_tool_input_json "$input")
        _allow_with_ids "$_ti" "$_sid"
      else
        allow_response
      fi
      exit 0
    fi

    _tool_pre_check "$input" "$tool_name" "$_original_hook_type"
    _forward_event_async "$_original_hook_type" "$input"

    if [[ "$TOOL_PRE_BLOCK" == "true" ]]; then
      deny_response "$TOOL_PRE_BLOCK_REASON" \
        "# Security Violation Detected

Your organization's security policy (enforced by Runlayer) has blocked this operation.

**What happened:**
- Violation type: Tool Input Policy
- Tool: ${tool_name}
- Reason: ${TOOL_PRE_BLOCK_REASON}

${_AGENT_GUARDRAILS}

**What to do:**
If you believe this is a false positive or mistake, contact your Runlayer administrator to review the security policy settings."
    fi

    _tool_pre_allow_response "$input"
    ;;

  # ---------------------------------------------------------------------------
  # PostToolUse — output scanning for Claude Code, Codex, and Cursor post hooks
  # ---------------------------------------------------------------------------
  PostToolUse|PostToolUseFailure)
    tool_name=$(echo "$input" | jq -r '.tool_name // empty' 2>/dev/null) || true

    if [[ "$_CLIENT" == "hermes" && "$_original_hook_type" == "post_tool_call" ]]; then
      if ! _is_mcp_tool "$tool_name"; then
        _tool_lifecycle_async "tool-post" "$input" "$tool_name" "$_original_hook_type"
      fi
      _forward_event_async "$_original_hook_type" "$input"
      exit 0
    fi

    if _is_mcp_tool "$tool_name"; then
      _forward_event_async "$_original_hook_type" "$input"
      if [[ "$_CLIENT" == "cursor" ]]; then
        echo "{}"
      fi
      exit 0
    fi

    if [[ "$_ENFORCEMENT" != "true" ]]; then
      _tool_lifecycle_async "tool-post" "$input" "$tool_name" "$_original_hook_type"
      _forward_event_async "$_original_hook_type" "$input"
      if [[ "$_CLIENT" == "cursor" ]]; then
        echo "{}"
      fi
      exit 0
    fi

    _tool_post_check "$input" "$_original_hook_type"
    _forward_event_async "$_original_hook_type" "$input"

    if [[ "$TOOL_POST_BLOCK" == "true" ]]; then
      block_output_response "$TOOL_POST_BLOCK_REASON"
    fi

    if [[ "$_CLIENT" == "cursor" ]]; then
      echo "{}"
    fi
    ;;

  # ---------------------------------------------------------------------------
  # beforeReadFile / beforeTabFileRead — Cursor-only; file_path at top level
  # ---------------------------------------------------------------------------
  beforeReadFile|beforeTabFileRead)
    if [[ "$_ENFORCEMENT" == "true" ]]; then
      file_path=$(echo "$input" | jq -r '.file_path // empty' 2>/dev/null) || true
      _check_file_read "$file_path"
    fi

    _forward_event_async "$_original_hook_type" "$input"
    allow_response
    ;;

  # ---------------------------------------------------------------------------
  # Stop — transcript attachment
  # ---------------------------------------------------------------------------
  Stop)
    _forward_stop_event "$_original_hook_type" "$input"
    if [[ "$_CLIENT" == "cursor" ]]; then
      _forward_cursor_stop_session_end "$input"
    fi
    allow_response
    ;;

  # ---------------------------------------------------------------------------
  # beforeShellExecution — Cursor-only; scan command for protected files
  # ---------------------------------------------------------------------------
  beforeShellExecution)
    if [[ "$_ENFORCEMENT" == "true" ]]; then
      shell_command=$(echo "$input" | jq -r '.command // empty' 2>/dev/null) || true
      _check_bash_command "$shell_command"
    fi
    _forward_event_async "$_original_hook_type" "$input"
    allow_response
    ;;

  # ---------------------------------------------------------------------------
  # PermissionRequest — Codex-only today; scan approval-bound shell command
  # ---------------------------------------------------------------------------
  PermissionRequest)
    if [[ "$_CLIENT" == "codex" && "$_ENFORCEMENT" == "true" ]]; then
      shell_command=$(echo "$input" | jq -r '.tool_input.command // empty' 2>/dev/null) || true
      _check_bash_command "$shell_command"
    fi
    _forward_event_async "$_original_hook_type" "$input"
    allow_response
    ;;

  # ---------------------------------------------------------------------------
  # Other blocking events — forward + allow
  # ---------------------------------------------------------------------------
  SubagentStart|UserPromptSubmit)
    # Event-only hooks are opt-in. Run them synchronously so clients that tear
    # down hook processes immediately do not drop the session pipeline event.
    if [[ "$hook_type" == "UserPromptSubmit" ]]; then
      _start_transcript_stream "$input"
    fi
    _forward_event "$_original_hook_type" "$input"
    allow_response
    ;;

  # ---------------------------------------------------------------------------
  # Observational events — forward only
  # ---------------------------------------------------------------------------
  *)
    _forward_event_async "$_original_hook_type" "$input"
    if [[ "$_CLIENT" == "cursor" ]]; then
      echo "{}"
    fi
    ;;
esac

exit 0
