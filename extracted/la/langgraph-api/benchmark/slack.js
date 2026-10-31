export const GREEN = "🟢";
export const YELLOW = "🟡";
export const RED = "🔴";

/** Links the commit that ran, not main, so a dispatch from a branch links a page that exists. */
export function footer(anchor, runUrl) {
  const ref = process.env.GITHUB_SHA || "main";
  const repo = process.env.GITHUB_REPOSITORY || "langchain-ai/langchainplus";
  const docs = `https://github.com/${repo}/blob/${ref}/langgraph-api/api/benchmark/REPORTS.md`;
  return [`<${docs}#${anchor}|What is this?>`, "details in thread", runUrl ? `<${runUrl}|Run>` : null].filter(Boolean).join(" · ");
}

/** Widest code-block line that stayed on one line in the Slack iPhone app at default text size; wider rows wrap. */
export const PHONE_WIDTH = 27;

export function widestCodeLine(text) {
  let inCode = false;
  let widest = 0;
  for (const line of text.split("\n")) {
    if (line.startsWith("```")) inCode = !inCode;
    else if (inCode) widest = Math.max(widest, [...line].length);
  }
  return widest;
}

export function dotFor({ failed, attention }) {
  if (failed) return RED;
  if (attention) return YELLOW;
  return GREEN;
}

async function post(token, channel, text, threadTs) {
  const body = { channel, text };
  if (threadTs) body.thread_ts = threadTs;
  const response = await fetch("https://slack.com/api/chat.postMessage", {
    method: "POST",
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(body),
  });
  // Slack rejects a bad payload with HTTP 200 and ok:false, so the status code
  // alone is not enough.
  const result = await response.json().catch(() => ({}));
  if (!result.ok) {
    throw new Error(`Slack API error: ${result.error ?? `HTTP ${response.status}`}`);
  }
  return result.ts;
}

/**
 * @param {{text: string, thread?: string[]}} report
 * @returns {Promise<boolean>} whether anything was posted
 */
export async function postReport({ text, thread = [] }) {
  const token = process.env.SLACK_BOT_TOKEN;
  const channel = process.env.SLACK_CHANNEL;
  if (!token || !channel) {
    console.log("SLACK_BOT_TOKEN or SLACK_CHANNEL not set; printing instead of posting");
    for (const part of [text, ...thread]) console.log(`${part}\n`);
    return false;
  }
  const ts = await post(token, channel, text);
  for (const reply of thread.filter(Boolean)) {
    await post(token, channel, reply, ts);
  }
  console.log(`Posted report to Slack with ${thread.length} thread repl${thread.length === 1 ? "y" : "ies"}`);
  return true;
}
