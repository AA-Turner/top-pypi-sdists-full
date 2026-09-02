// Minimal LangChainGo agent with tools (framework detection corpus).
package main

import (
	"context"
	"fmt"
	"log"

	"github.com/tmc/langchaingo/agents"
	"github.com/tmc/langchaingo/chains"
	"github.com/tmc/langchaingo/llms/openai"
	"github.com/tmc/langchaingo/tools"
)

type getWeather struct{}

func (t getWeather) Name() string { return "get_weather" }

func (t getWeather) Description() string {
	return "Get the current weather for a city. Input is the city name."
}

func (t getWeather) Call(_ context.Context, input string) (string, error) {
	return fmt.Sprintf("It's 72F and sunny in %s.", input), nil
}

type add struct{}

func (t add) Name() string { return "add" }

func (t add) Description() string {
	return "Add two integers. Input is two integers separated by a space."
}

func (t add) Call(_ context.Context, input string) (string, error) {
	var a, b int
	if _, err := fmt.Sscanf(input, "%d %d", &a, &b); err != nil {
		return "", err
	}
	return fmt.Sprintf("%d", a+b), nil
}

func main() {
	llm, err := openai.New(openai.WithModel("gpt-4o-mini"))
	if err != nil {
		log.Fatal(err)
	}

	agentTools := []tools.Tool{getWeather{}, add{}}
	agent := agents.NewOneShotAgent(llm, agentTools)
	executor := agents.NewExecutor(agent)

	answer, err := chains.Run(
		context.Background(),
		executor,
		"What's the weather in Paris, and what is 21 + 21?",
	)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println(answer)
}
