/** Minimal OpenAI Agents SDK (JS) agent (framework detection corpus). */

import { Agent, run, tool } from "@openai/agents";
import { z } from "zod";

const getWeather = tool({
  name: "get_weather",
  description: "Get the current weather for a city.",
  parameters: z.object({ city: z.string() }),
  execute: async ({ city }) => `It's 72F and sunny in ${city}.`,
});

const add = tool({
  name: "add",
  description: "Add two integers.",
  parameters: z.object({ a: z.number(), b: z.number() }),
  execute: async ({ a, b }) => `${a + b}`,
});

async function main(): Promise<void> {
  const agent = new Agent({
    name: "Assistant",
    instructions: "You are a helpful assistant. Use tools when needed.",
    tools: [getWeather, add],
  });
  const result = await run(
    agent,
    "What's the weather in Paris, and what is 21 + 21?",
  );
  console.log(result.finalOutput);
}

void main();
