from grazie.api.client.parameters import Parameters


class BaseParameters:
    # Temperature of generation
    Temperature = Parameters.FloatKey("llm.parameters.temperature")

    # Max length of generated text in tokens
    Length = Parameters.IntKey("llm.parameters.length")

    # Stop token to stop generation at. Token may contain more than one character.
    StopToken = Parameters.StrKey("llm.parameters.stop-token")

    # Restrict repetition of ngrams of no-repeat size
    NoRepeat = Parameters.IntKey("llm.parameters.no-repeat")

    # Nucleus sampling, where the model considers the results of the tokens with topP probability mass.
    TopP = Parameters.FloatKey("llm.parameters.top-p")

    # Only sample from the top K options for each subsequent token. Used to remove "long tail" low probability responses.
    TopK = Parameters.IntKey("llm.parameters.top-k")

    # The number of dimensions the resulting output embeddings should have
    Dimension = Parameters.IntKey("llm.parameters.dimension")

    # Controls the output mode to constrain the model to generate strings that parse into valid JSON objects or plain text.
    ResponseFormat = Parameters.JsonKey("llm.parameters.response-format")

    # Random number generator for the language model. Essential for ensuring reproducibility of outcomes.
    Seed = Parameters.IntKey("llm.parameters.seed")


class LLMParameters(BaseParameters):
    # List of functions to use in generation
    Functions = Parameters.JsonKey("llm.parameters.functions")

    # Function call mode
    FunctionCall = Parameters.JsonKey("llm.parameters.function.mode")
