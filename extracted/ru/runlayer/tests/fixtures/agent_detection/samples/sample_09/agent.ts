/** Minimal LangChain.js ReAct agent (framework detection corpus). */

import { tool } from "@langchain/core/tools";
import { createReactAgent } from "@langchain/langgraph/prebuilt";
import { ChatOpenAI } from "@langchain/openai";
import { z } from "zod";

const getWeather = tool(
  async ({ city }: { city: string }) => `It's 72F and sunny in ${city}.`,
  {
    name: "get_weather",
    description: "Get the current weather for a city.",
    schema: z.object({ city: z.string() }),
  },
);

const add = tool(
  async ({ a, b }: { a: number; b: number }) => `${a + b}`,
  {
    name: "add",
    description: "Add two integers.",
    schema: z.object({ a: z.number(), b: z.number() }),
  },
);

async function main(): Promise<void> {
  const llm = new ChatOpenAI({ model: "gpt-4o-mini" });
  const agent = createReactAgent({ llm, tools: [getWeather, add] });
  const result = await agent.invoke({
    messages: [
      {
        role: "user",
        content: "What's the weather in Paris, and what is 21 + 21?",
      },
    ],
  });
  console.log(result.messages[result.messages.length - 1].content);
}

void main();
