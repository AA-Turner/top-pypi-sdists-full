// Minimal Semantic Kernel agent with tools (framework detection corpus).
using System.ComponentModel;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;
using Microsoft.SemanticKernel.Connectors.OpenAI;

class WeatherAndMathPlugin
{
    [KernelFunction("get_weather")]
    [Description("Get the current weather for a city.")]
    public string GetWeather(string city) => $"It's 72F and sunny in {city}.";

    [KernelFunction("add")]
    [Description("Add two integers.")]
    public int Add(int a, int b) => a + b;
}

class Program
{
    static async Task Main()
    {
        var builder = Kernel.CreateBuilder();
        builder.AddOpenAIChatCompletion(
            modelId: "gpt-4o-mini",
            apiKey: Environment.GetEnvironmentVariable("OPENAI_API_KEY") ?? "");
        builder.Plugins.AddFromType<WeatherAndMathPlugin>();
        Kernel kernel = builder.Build();

        OpenAIPromptExecutionSettings settings = new()
        {
            FunctionChoiceBehavior = FunctionChoiceBehavior.Auto()
        };

        var chat = kernel.GetRequiredService<IChatCompletionService>();
        ChatHistory history = new("You are a helpful assistant. Use tools when needed.");
        history.AddUserMessage("What's the weather in Paris, and what is 21 + 21?");

        var result = await chat.GetChatMessageContentAsync(history, settings, kernel);
        Console.WriteLine(result.Content);
    }
}
