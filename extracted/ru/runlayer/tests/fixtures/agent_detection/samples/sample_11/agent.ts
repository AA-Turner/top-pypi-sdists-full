/** Minimal Vercel AI SDK tool-using agent (framework detection corpus). */

import { openai } from "@ai-sdk/openai";
import { generateText, stepCountIs, tool } from "ai";
import { z } from "zod";

async function main(): Promise<void> {
  const result = await generateText({
    model: openai("gpt-4o-mini"),
    system: "You are a helpful assistant. Use tools when needed.",
    prompt: "What's the weather in Paris, and what is 21 + 21?",
    stopWhen: stepCountIs(5),
    tools: {
      get_weather: tool({
        description: "Get the current weather for a city.",
        inputSchema: z.object({ city: z.string() }),
        execute: async ({ city }) => `It's 72F and sunny in ${city}.`,
      }),
      add: tool({
        description: "Add two integers.",
        inputSchema: z.object({ a: z.number(), b: z.number() }),
        execute: async ({ a, b }) => `${a + b}`,
      }),
    },
  });
  console.log(result.text);
}

void main();
