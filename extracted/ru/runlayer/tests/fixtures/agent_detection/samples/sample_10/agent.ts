/** Minimal Mastra agent with tools (framework detection corpus). */

import { openai } from "@ai-sdk/openai";
import { Mastra } from "@mastra/core";
import { Agent } from "@mastra/core/agent";
import { createTool } from "@mastra/core/tools";
import { z } from "zod";

const getWeather = createTool({
  id: "get_weather",
  description: "Get the current weather for a city.",
  inputSchema: z.object({ city: z.string() }),
  execute: async ({ context }) => `It's 72F and sunny in ${context.city}.`,
});

const add = createTool({
  id: "add",
  description: "Add two integers.",
  inputSchema: z.object({ a: z.number(), b: z.number() }),
  execute: async ({ context }) => `${context.a + context.b}`,
});

const assistant = new Agent({
  name: "assistant",
  instructions: "You are a helpful assistant. Use tools when needed.",
  model: openai("gpt-4o-mini"),
  tools: { getWeather, add },
});

export const mastra = new Mastra({ agents: { assistant } });

async function main(): Promise<void> {
  const agent = mastra.getAgent("assistant");
  const result = await agent.generate(
    "What's the weather in Paris, and what is 21 + 21?",
  );
  console.log(result.text);
}

void main();
