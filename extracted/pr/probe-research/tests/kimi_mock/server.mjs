// A scripted stand-in for an OpenAI-compatible chat-completions model, so the
// real Kimi Code CLI can run end to end with no account and no model spend.
// Used to record the Kimi fixtures and by the weekly Kimi canary.
//
// The newest real user prompt is the script, one directive per line (or per
// ` ;; ` on one line, for the interactive TUI):
//   RUN: <shell command>        -> a Bash tool call
//   WRITE: <path> :: <content>  -> a Write tool call
//   ASK                         -> an AskUserQuestion call
//   SUB                         -> an Agent (subagent) call
//   SAY: <text>                 -> the final reply (default "Done.")
// Each tool round of the turn takes the next directive; when none are left the
// model answers with the SAY text. A subagent's own prompt gets a plain reply.
//
// Run: MOCK_PORT=18765 node server.mjs   (MOCK_LOG=<file> records requests)
import fs from 'node:fs';
import http from 'node:http';

const PORT = Number(process.env.MOCK_PORT ?? 18765);
const LOG = process.env.MOCK_LOG ?? '';
let counter = 0;

function textOf(content) {
  if (typeof content === 'string') return content;
  if (Array.isArray(content)) return content.map((part) => part?.text ?? '').join('\n');
  return '';
}

// Injected user-role text (system reminders, hook results) is not the script.
function isInjected(text) {
  const head = text.trimStart();
  return head.startsWith('<system-reminder>') || head.startsWith('<hook_result') || head.startsWith('<system>');
}

function scriptOf(messages) {
  let index = -1;
  for (let i = messages.length - 1; i >= 0; i -= 1) {
    const message = messages[i];
    if (message.role !== 'user') continue;
    const text = textOf(message.content);
    if (isInjected(text)) continue;
    if (/(^|;; )(RUN|WRITE|SAY):|(^|;; )(ASK|SUB)(\s|$)/m.test(text)) {
      index = i;
      break;
    }
    if (index === -1) index = i;
    break;
  }
  if (index === -1) return { lines: [], done: 0 };
  const lines = textOf(messages[index].content)
    .split(/\n| ;; /)
    .map((line) => line.trim())
    .filter((line) => /^(RUN|WRITE|SAY):|^(ASK|SUB)$/.test(line));
  const done = messages.slice(index + 1).filter((m) => m.role === 'tool').length;
  return { lines, done };
}

function plan(body) {
  const messages = body.messages ?? [];
  if (!Array.isArray(body.tools) || body.tools.length === 0) return { text: 'Kimi fixture session' };
  const { lines, done } = scriptOf(messages);
  const steps = lines.filter((line) => !line.startsWith('SAY:'));
  const say = (lines.find((line) => line.startsWith('SAY:')) ?? 'SAY: Done.').slice(4).trim();
  if (lines.length === 0) return { reasoning: 'A plain question; answer it.', text: 'Hello from the mock model.' };
  if (done >= steps.length) return { reasoning: 'Every step ran; wrap up.', text: say };
  const step = steps[done];
  if (step.startsWith('RUN:')) {
    const command = step.slice(4).trim();
    return { reasoning: `Run: ${command}`, text: 'Running a command.', tool: { name: 'Bash', args: { command } } };
  }
  if (step.startsWith('WRITE:')) {
    const [path, content = ''] = step.slice(6).split('::').map((part) => part.trim());
    return { reasoning: `Write ${path}`, text: 'Writing a file.', tool: { name: 'Write', args: { path, content } } };
  }
  if (step === 'ASK') {
    return {
      reasoning: 'Ask the researcher.',
      text: 'One question first.',
      tool: {
        name: 'AskUserQuestion',
        args: {
          questions: [
            {
              question: 'Which learning rate should the sweep start from?',
              header: 'LR',
              options: [
                { label: '3e-4', description: 'the usual default' },
                { label: '1e-3', description: 'faster, riskier' },
              ],
              multi_select: false,
            },
          ],
        },
      },
    };
  }
  return {
    reasoning: 'Delegate a small check.',
    text: 'Delegating.',
    tool: { name: 'Agent', args: { description: 'quick check', prompt: 'Reply with ok.', subagent_type: 'coder' } },
  };
}

function send(res, body, choice) {
  const id = `chatcmpl-${counter}`;
  const created = Math.floor(Date.now() / 1000);
  const usage = { prompt_tokens: 100, completion_tokens: 10, total_tokens: 110 };
  const toolCalls = choice.tool
    ? [{ index: 0, id: `call_${counter}`, type: 'function', function: { name: choice.tool.name, arguments: JSON.stringify(choice.tool.args) } }]
    : undefined;
  const finish = choice.tool ? 'tool_calls' : 'stop';
  if (!body.stream) {
    const message = { role: 'assistant', content: choice.text ?? '' };
    if (choice.reasoning) message.reasoning_content = choice.reasoning;
    if (toolCalls) message.tool_calls = toolCalls.map(({ index, ...call }) => call);
    res.writeHead(200, { 'content-type': 'application/json' });
    res.end(JSON.stringify({ id, object: 'chat.completion', created, model: body.model, choices: [{ index: 0, message, finish_reason: finish }], usage }));
    return;
  }
  const base = { id, object: 'chat.completion.chunk', created, model: body.model };
  const chunk = (delta, extra = {}) => res.write(`data: ${JSON.stringify({ ...base, choices: [{ index: 0, delta, ...extra }] })}\n\n`);
  res.writeHead(200, { 'content-type': 'text/event-stream' });
  chunk({ role: 'assistant' });
  if (choice.reasoning) chunk({ reasoning_content: choice.reasoning });
  if (choice.text) chunk({ content: choice.text });
  if (toolCalls) chunk({ tool_calls: toolCalls });
  res.write(`data: ${JSON.stringify({ ...base, choices: [{ index: 0, delta: {}, finish_reason: finish }], usage })}\n\n`);
  res.write('data: [DONE]\n\n');
  res.end();
}

http
  .createServer((req, res) => {
    let raw = '';
    req.on('data', (chunk) => {
      raw += chunk;
    });
    req.on('end', () => {
      counter += 1;
      let body = {};
      try {
        body = raw ? JSON.parse(raw) : {};
      } catch {
        body = {};
      }
      if (LOG) fs.appendFileSync(LOG, `${JSON.stringify({ n: counter, url: req.url, body })}\n`);
      if (req.method === 'GET' && req.url.endsWith('/models')) {
        res.writeHead(200, { 'content-type': 'application/json' });
        res.end(JSON.stringify({ object: 'list', data: [{ id: 'mock-model', object: 'model' }] }));
        return;
      }
      if (!req.url.endsWith('/chat/completions')) {
        res.writeHead(404);
        res.end('{}');
        return;
      }
      send(res, body, plan(body));
    });
  })
  .listen(PORT, '127.0.0.1', () => process.stdout.write(`kimi mock model on ${PORT}\n`));
