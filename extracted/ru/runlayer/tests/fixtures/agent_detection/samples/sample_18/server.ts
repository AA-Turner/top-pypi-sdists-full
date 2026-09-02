import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";

const server = new McpServer({ name: "sample", version: "1.0.0" });

server.registerTool(
  "echo",
  { inputSchema: { message: "string" } },
  async ({ message }) => ({ content: [{ type: "text", text: message }] }),
);
