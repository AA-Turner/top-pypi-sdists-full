// Minimal LangChain4j AI Service with tools (framework detection corpus).
package com.example;

import dev.langchain4j.agent.tool.Tool;
import dev.langchain4j.model.chat.ChatModel;
import dev.langchain4j.model.openai.OpenAiChatModel;
import dev.langchain4j.service.AiServices;
import dev.langchain4j.service.SystemMessage;

public class Main {

    static class Tools {
        @Tool("Get the current weather for a city.")
        String getWeather(String city) {
            return "It's 72F and sunny in " + city + ".";
        }

        @Tool("Add two integers.")
        int add(int a, int b) {
            return a + b;
        }
    }

    interface Assistant {
        @SystemMessage("You are a helpful assistant. Use tools when needed.")
        String chat(String userMessage);
    }

    public static void main(String[] args) {
        ChatModel model = OpenAiChatModel.builder()
                .apiKey(System.getenv("OPENAI_API_KEY"))
                .modelName("gpt-4o-mini")
                .build();

        Assistant assistant = AiServices.builder(Assistant.class)
                .chatModel(model)
                .tools(new Tools())
                .build();

        String answer = assistant.chat("What's the weather in Paris, and what is 21 + 21?");
        System.out.println(answer);
    }
}
