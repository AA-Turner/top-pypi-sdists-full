// Minimal Spring AI ChatClient agent with tools (framework detection corpus).
package com.example;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.openai.OpenAiChatModel;
import org.springframework.ai.openai.api.OpenAiApi;
import org.springframework.ai.tool.annotation.Tool;

public class Main {

    static class WeatherAndMathTools {
        @Tool(description = "Get the current weather for a city.")
        String getWeather(String city) {
            return "It's 72F and sunny in " + city + ".";
        }

        @Tool(description = "Add two integers.")
        int add(int a, int b) {
            return a + b;
        }
    }

    public static void main(String[] args) {
        OpenAiApi openAiApi = OpenAiApi.builder()
                .apiKey(System.getenv("OPENAI_API_KEY"))
                .build();

        OpenAiChatModel chatModel = OpenAiChatModel.builder()
                .openAiApi(openAiApi)
                .build();

        ChatClient chatClient = ChatClient.create(chatModel);

        String answer = chatClient.prompt()
                .system("You are a helpful assistant. Use tools when needed.")
                .user("What's the weather in Paris, and what is 21 + 21?")
                .tools(new WeatherAndMathTools())
                .call()
                .content();

        System.out.println(answer);
    }
}
