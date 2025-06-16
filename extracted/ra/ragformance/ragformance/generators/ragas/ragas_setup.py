import importlib
import subprocess
import sys
from typing import Optional, List
import inspect
import warnings
import os

try:
    from ragas.embeddings import LangchainEmbeddingsWrapper
    from ragas.llms import LangchainLLMWrapper
    from ragas.testset import TestsetGenerator
    from ragas.testset.synthesizers.multi_hop import (
        MultiHopAbstractQuerySynthesizer,
        MultiHopSpecificQuerySynthesizer,
    )
    from ragas.testset.synthesizers.single_hop.specific import (
        SingleHopSpecificQuerySynthesizer,
    )
    from ragas.testset.synthesizers import QueryDistribution

    _RAGAS_AVAILABLE = True
except ImportError:
    _RAGAS_AVAILABLE = False
    LangchainEmbeddingsWrapper = None
    LangchainLLMWrapper = None
    TestsetGenerator = None
    MultiHopAbstractQuerySynthesizer = None
    MultiHopSpecificQuerySynthesizer = None
    SingleHopSpecificQuerySynthesizer = None
    QueryDistribution = None

# Pipeline id from the config .json
PIPELINE_ID = "ragas"

# Provider: (pip_package, chat_module, chat_class, embeddings_module, embeddings_class)
PROVIDER_REGISTRY = {
    "openai": (
        "langchain-openai",
        "langchain_openai.chat_models",
        "ChatOpenAI",
        "langchain_openai.embeddings",
        "OpenAIEmbeddings",
    ),
    "anthropic": (
        "langchain-anthropic",
        "langchain_anthropic.chat_models",
        "ChatAnthropic",
        "langchain_anthropic.embeddings",
        "AnthropicEmbeddings",
    ),
    "mistralai": (
        "langchain-mistralai",
        "langchain_mistralai.chat_models",
        "ChatMistralAI",
        "langchain_mistralai.embeddings",
        "MistralAIEmbeddings",
    ),
    "groq": (
        "langchain-groq",
        "langchain_groq.chat_models",
        "ChatGroq",
        "langchain_groq.embeddings",
        "GroqEmbeddings",
    ),
    "ollama": (
        "langchain-ollama",
        "langchain_ollama.chat_models",
        "ChatOllama",
        "langchain_ollama.embeddings",
        "OllamaEmbeddings",
    ),
    "huggingface": (
        "langchain-huggingface",
        "langchain_huggingface.chat_models",
        "ChatHuggingFace",
        "langchain_huggingface.embeddings",
        "HuggingFaceEmbeddings",
    ),
    "fireworks": (
        "langchain-fireworks",
        "langchain_fireworks.chat_models",
        "ChatFireworks",
        "langchain_fireworks.embeddings",
        "FireworksEmbeddings",
    ),
    "deepseek": (
        "langchain-deepseek",
        "langchain_deepseek.chat_models",
        "ChatDeepSeek",
        "langchain_deepseek.embeddings",
        "DeepSeekEmbeddings",
    ),
    "perplexity": (
        "langchain-perplexity",
        "langchain_perplexity.chat_models",
        "ChatPerplexity",
        "langchain_perplexity.embeddings",
        "PerplexityEmbeddings",
    ),
    "xai": (
        "langchain-xai",
        "langchain_xai.chat_models",
        "ChatXAI",
        "langchain_xai.embeddings",
        "XAIEmbeddings",
    ),
    "cohere": (
        "langchain-cohere",
        "langchain_cohere.chat_models",
        "ChatCohere",
        "langchain_cohere.embeddings",
        "CohereEmbeddings",
    ),
    "together": (
        "langchain-together",
        "langchain_together.chat_models",
        "ChatTogether",
        "langchain_together.embeddings",
        "TogetherEmbeddings",
    ),
    "litellm": (
        "langchain-community",  # ChatLiteLLM is in langchain-community
        "langchain_community.chat_models.litellm",
        "ChatLiteLLM",
        "langchain_openai.embeddings",  # Placeholder, assuming embeddings might be separate
        "OpenAIEmbeddings",  # Placeholder
    ),
    # Extend as needed
}

# Map the JSON question_type → your classes
QUESTION_SYNTHESIZERS = {
    "singlehop-specific": SingleHopSpecificQuerySynthesizer,
    "multihop-specific": MultiHopSpecificQuerySynthesizer,
    "multihop-abstract": MultiHopAbstractQuerySynthesizer,
}


def _validate_langchain_args(provider, class_instance, class_type, **kwargs):
    # The additional arguments must comply with the obtained llmchat class from langchain

    if class_type == "llm":
        JSON_TARGET_FIELD = "llms"
    elif class_type == "embedding":
        JSON_TARGET_FIELD = "embeddings"

    # Get the signature of the method
    sig = inspect.signature(class_instance)

    # Get arguments from the method TestsetGenerator.generate
    valid_arg_names = [
        name
        for name in sig.parameters
        if name != "self"  # usually omit 'self'
    ]

    valid_arg_aliases = [
        field.alias
        for name, field in class_instance.__fields__.items()
        if field.alias and field.alias != name
    ]

    valid_arg_names += valid_arg_aliases

    # Find any unexpected arguments on **kwargs[langchain_provider]

    unexpected_langchain_args = [
        key for key in kwargs["langchain_provider"] if key not in valid_arg_names
    ]

    if unexpected_langchain_args:
        raise ValueError(
            f"\n RAGAS-ERROR: {class_instance} with unexpected argument(s) : {', '.join(unexpected_langchain_args)}.\n"
            f"Valid arguments for {class_instance} are: {', '.join(sorted(valid_arg_names))}\n\n"
            f"Please, correct the config.json file: \n"
            f"\t - Locate the {JSON_TARGET_FIELD} with provider '{provider}'\n"
            f"\t - In 'params':{{'...'langchain_provider': ...}} \n"
            f"\t - Fields must comply with the valid argument list above\n"
        )

    # Find any unexpected arguments from the rest of common **kwargs
    # kwargs here is expected to be the "params" dictionary from the config.
    # It might contain 'langchain_provider' as a key for nested specific args.

    langchain_provider_params = kwargs.get("langchain_provider", {})
    common_params_from_config = {
        k: v
        for k, v in kwargs.items()
        if k not in ["langchain_provider", "langchain_rate_limiter"]
    }

    # Validate langchain_provider specific arguments
    unexpected_langchain_args = [
        key for key in langchain_provider_params if key not in valid_arg_names
    ]
    if unexpected_langchain_args:
        raise ValueError(
            f"\n RAGAS-ERROR: {class_instance} with unexpected 'langchain_provider' argument(s) : {', '.join(unexpected_langchain_args)}.\n"
            f"Valid arguments for {class_instance} are: {', '.join(sorted(valid_arg_names))}\n\n"
            f"Please, correct your config: \n"
            f"\t - Provider '{provider}', in 'params', key 'langchain_provider'.\n"
            f"\t - Fields must comply with the valid argument list above.\n"
        )

    # Validate common arguments (those not under 'langchain_provider')
    unexpected_common_args = [
        key for key in common_params_from_config if key not in valid_arg_names
    ]
    if unexpected_common_args:
        warnings.warn(
            f"\n RAGAS-WARNING: {class_instance} will IGNORE common argument(s) from 'params': {', '.join(unexpected_common_args)}.\n"
            f"Valid arguments for {class_instance} are: {', '.join(sorted(valid_arg_names))}\n\n"
            f"If these arguments are specific to the Langchain provider, move them under 'langchain_provider' in your config."
        )

    # Combine valid parameters
    final_valid_kwargs = {}
    for key, value in common_params_from_config.items():
        if key in valid_arg_names and value is not None:
            final_valid_kwargs[key] = value

    for key, value in langchain_provider_params.items():
        if (
            key in valid_arg_names and value is not None
        ):  # Ensure not to overwrite a common valid param with a langchain_provider one if names clash and both are valid
            if key in final_valid_kwargs:
                warnings.warn(
                    f"Parameter '{key}' is defined in both common params and langchain_provider params. Using value from langchain_provider_params."
                )
            final_valid_kwargs[key] = value

    return final_valid_kwargs


def get_configured_llm(llm_config: dict) -> LangchainLLMWrapper:
    if not _RAGAS_AVAILABLE:
        raise ImportError(
            "'ragas' module is not installed. "
            "Please install ragformance with the [generators-ragas] option:\n"
            "    pip install ragformance[generators-ragas]"
        )
    """
    Configures and returns a LangchainLLMWrapper for RAGAS based on dictionary config.
    llm_config schema:
    {
        "name": "llm_name",
        "provider": "openai",
        "model": "gpt-3.5-turbo",
        "api_key_env": "YOUR_ENV_VAR_FOR_API_KEY", (optional)
        "base_url": "...", (optional)
        "params": {
            "temperature": 0.7,
            "langchain_provider": {"max_tokens": 1000} (optional)
        } (optional)
    }
    """
    provider = llm_config["provider"]
    model_name_str = llm_config["model"]  # This is the specific model identifier string
    api_key = (
        os.getenv(llm_config["api_key_env"]) if "api_key_env" in llm_config else None
    )
    base_url = llm_config.get("base_url")
    config_params = llm_config.get("params", {})

    if provider not in PROVIDER_REGISTRY:
        raise ValueError(f"Unknown LLM provider: {provider}")

    _pip_package, chat_module_path, chat_class_name, _embed_module, _embed_class = (
        PROVIDER_REGISTRY[provider]
    )

    try:
        chat_module = importlib.import_module(chat_module_path)
    except ImportError:
        print(f"Installing missing package for LLM provider {provider}: {_pip_package}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", _pip_package])
        chat_module = importlib.import_module(chat_module_path)

    ChatClass = getattr(chat_module, chat_class_name)

    # Prepare kwargs for the Langchain ChatClass constructor
    # Start with essential, then add from params
    constructor_kwargs = {
        "model": model_name_str
    }  # For many, model is 'model' or 'model_name'
    if (
        provider == "ollama" or provider == "openai" or provider == "mistralai"
    ):  # these often use model_name
        constructor_kwargs["model_name"] = (
            model_name_str  # Some like OpenAI use model_name
        )

    if api_key:
        constructor_kwargs["api_key"] = api_key
    if base_url:
        constructor_kwargs["base_url"] = base_url

    # Merge with validated params from config_params
    # _validate_langchain_args expects the full params dict (which might include 'langchain_provider')
    validated_params = _validate_langchain_args(
        provider, ChatClass, class_type="llm", **config_params
    )
    constructor_kwargs.update(validated_params)

    # Ensure 'model' or 'model_name' is correctly set based on provider needs, overriding if necessary from validated_params
    # if 'model' in validated_params or 'model_name' in validated_params:
    #    pass # Already handled by validated_params update if they were valid
    if (
        provider == "litellm"
    ):  # ChatLiteLLM specifically uses 'model' for the full model string
        constructor_kwargs["model"] = model_name_str
        # And it needs api_key and base_url passed explicitly if they are part of its signature.
        # _validate_langchain_args should handle this if api_key/base_url are valid params for ChatLiteLLM.

    print(f"Instantiating {ChatClass.__name__} with: {constructor_kwargs}")
    langchain_llm = ChatClass(**constructor_kwargs)
    return LangchainLLMWrapper(langchain_llm)


def get_configured_embeddings(embedding_config: dict) -> LangchainEmbeddingsWrapper:
    if not _RAGAS_AVAILABLE:
        raise ImportError(
            "'ragas' module is not installed. "
            "Please install ragformance with the [generators-ragas] option:\n"
            "    pip install ragformance[generators-ragas]"
        )
    """
    Configures and returns a LangchainEmbeddingsWrapper for RAGAS based on dictionary config.
    embedding_config schema:
    {
        "name": "embedding_model_name",
        "provider": "openai",
        "model": "text-embedding-ada-002",
        "api_key_env": "YOUR_ENV_VAR_FOR_API_KEY", (optional)
        "base_url": "...", (optional)
        "params": {
             "langchain_provider": {} (optional)
        } (optional)
    }
    """
    provider = embedding_config["provider"]
    model_name_str = embedding_config["model"]
    api_key = (
        os.getenv(embedding_config["api_key_env"])
        if "api_key_env" in embedding_config
        else None
    )
    base_url = embedding_config.get("base_url")
    config_params = embedding_config.get("params", {})

    if provider not in PROVIDER_REGISTRY:
        raise ValueError(f"Unknown Embeddings provider: {provider}")

    _pip_package, _chat_module, _chat_class, embed_module_path, embed_class_name = (
        PROVIDER_REGISTRY[provider]
    )

    try:
        embed_module = importlib.import_module(embed_module_path)
    except ImportError:
        print(
            f"Installing missing package for Embeddings provider {provider}: {_pip_package}"
        )
        subprocess.check_call([sys.executable, "-m", "pip", "install", _pip_package])
        embed_module = importlib.import_module(embed_module_path)

    EmbeddingsClass = getattr(embed_module, embed_class_name)

    constructor_kwargs = {"model": model_name_str}
    if provider == "openai":  # OpenAIEmbeddings uses model
        constructor_kwargs["model"] = model_name_str
    elif provider == "huggingface":  # HuggingFaceEmbeddings uses model_name
        constructor_kwargs = {"model_name": model_name_str}

    if api_key:
        constructor_kwargs["api_key"] = api_key
    if base_url:
        constructor_kwargs["base_url"] = base_url

    validated_params = _validate_langchain_args(
        provider, EmbeddingsClass, class_type="embedding", **config_params
    )
    constructor_kwargs.update(validated_params)

    print(f"Instantiating {EmbeddingsClass.__name__} with: {constructor_kwargs}")
    langchain_embeddings = EmbeddingsClass(**constructor_kwargs)
    return LangchainEmbeddingsWrapper(langchain_embeddings)


def get_ragas_testset_generator(
    llm: LangchainLLMWrapper,
    embeddings: LangchainEmbeddingsWrapper,
    critique_llm: Optional[LangchainLLMWrapper] = None,
) -> TestsetGenerator:
    """
    Creates a RAGAS TestsetGenerator instance.
    """
    # RAGAS TestsetGenerator expects 'generator_llm', 'critic_llm', 'embeddings'
    return TestsetGenerator(
        generator_llm=llm,
        critic_llm=critique_llm
        if critique_llm
        else llm,  # Use generator_llm if no specific critic_llm
        embeddings=embeddings,
    )


def get_configured_query_distribution(
    distribution_config_list: List[dict], llm: LangchainLLMWrapper
) -> QueryDistribution:
    """
    Creates a RAGAS QueryDistribution from a list of configuration dictionaries.
    distribution_config_list item schema:
    {
        "type": "singlehop-specific",
        "ratio": 0.5
        # "prompt": "Optional custom prompt string for this synthesizer" # Not directly supported by RAGAS synthesizers
    }
    """
    dist: QueryDistribution = []
    for item in distribution_config_list:
        q_type = item["type"]
        ratio = item["ratio"]

        SynthesizerClass = QUESTION_SYNTHESIZERS.get(q_type)
        if SynthesizerClass is None:
            raise ValueError(
                f"RAGAS Config Error: Unknown question_type '{q_type}' in question_distribution."
            )

        synthesizer_instance = SynthesizerClass(llm=llm)
        dist.append((synthesizer_instance, ratio))
    return dist
