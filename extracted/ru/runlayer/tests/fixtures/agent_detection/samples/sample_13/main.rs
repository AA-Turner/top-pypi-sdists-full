//! Minimal Rig agent with tools (framework detection corpus).

use rig::completion::Prompt;
use rig::providers::openai;
use rig::tool::Tool;
use serde::{Deserialize, Serialize};
use serde_json::json;

#[derive(Deserialize)]
struct WeatherArgs {
    city: String,
}

#[derive(Deserialize)]
struct AddArgs {
    a: i64,
    b: i64,
}

#[derive(Debug, thiserror::Error)]
#[error("tool error")]
struct ToolError;

#[derive(Serialize)]
struct GetWeather;

impl Tool for GetWeather {
    const NAME: &'static str = "get_weather";
    type Error = ToolError;
    type Args = WeatherArgs;
    type Output = String;

    async fn definition(&self, _prompt: String) -> rig::completion::ToolDefinition {
        rig::completion::ToolDefinition {
            name: Self::NAME.to_string(),
            description: "Get the current weather for a city.".to_string(),
            parameters: json!({
                "type": "object",
                "properties": { "city": { "type": "string" } },
                "required": ["city"]
            }),
        }
    }

    async fn call(&self, args: Self::Args) -> Result<Self::Output, Self::Error> {
        Ok(format!("It's 72F and sunny in {}.", args.city))
    }
}

#[derive(Serialize)]
struct Add;

impl Tool for Add {
    const NAME: &'static str = "add";
    type Error = ToolError;
    type Args = AddArgs;
    type Output = i64;

    async fn definition(&self, _prompt: String) -> rig::completion::ToolDefinition {
        rig::completion::ToolDefinition {
            name: Self::NAME.to_string(),
            description: "Add two integers.".to_string(),
            parameters: json!({
                "type": "object",
                "properties": {
                    "a": { "type": "integer" },
                    "b": { "type": "integer" }
                },
                "required": ["a", "b"]
            }),
        }
    }

    async fn call(&self, args: Self::Args) -> Result<Self::Output, Self::Error> {
        Ok(args.a + args.b)
    }
}

#[tokio::main]
async fn main() -> Result<(), anyhow::Error> {
    let client = openai::Client::from_env();
    let agent = client
        .agent("gpt-4o-mini")
        .preamble("You are a helpful assistant. Use tools when needed.")
        .tool(GetWeather)
        .tool(Add)
        .build();

    let response = agent
        .prompt("What's the weather in Paris, and what is 21 + 21?")
        .await?;

    println!("{response}");
    Ok(())
}
