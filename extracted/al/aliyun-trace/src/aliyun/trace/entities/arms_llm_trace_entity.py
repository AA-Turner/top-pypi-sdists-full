from pydantic import BaseModel, Field
# from pydantic_core.core_schema import ValidationInfo
from typing import Optional, List, Any
from aliyun.semconv.trace import SpanAttributes, AliyunSpanKindValues, EmbeddingAttributes, MessageAttributes, \
    DocumentAttributes, RerankerAttributes
from abc import abstractmethod
from aliyun.trace.utils import add_attribute


class LLMBaseModel(BaseModel):
    response_id: Optional[str] = Field(default=None, description="response id", examples="12345564")

    def get_type(self) -> str:
        return self._get_type()

    def get_attributes(self) -> dict:
        common_attr = self._get_common_attr()
        attr = self._get_attributes()
        if len(common_attr) > 0:
            attr.update(common_attr)
        return attr

    def _get_common_attr(self) -> dict:
        attributes = {}
        # add_attribute(attributes, SpanAttributes.GEN_AI_SPAN_KIND, AliyunSpanKindValues.LLM.value)
        if self.response_id is not None:
            add_attribute(attributes, "gen_ai.response.id", self.response_id)
        return attributes

    @abstractmethod
    def _get_type(self) -> str:
        pass

    @abstractmethod
    def _get_attributes(self) -> dict:
        pass


class Resource(BaseModel):
    host_name: Optional[str] = Field(None,
                                     description="host name")
    service_name: Optional[str] = Field(None,
                                        description="service name")
    service_version: Optional[str] = Field(None,
                                           description="service version")
    service_owner_sub_id: Optional[str] = Field(None,
                                                description="service.owner.sub_id")
    service_app_name: Optional[str] = Field(None,
                                            description="service.app.name")
    service_app_owner_id: Optional[str] = Field(None,
                                                description="service.app.owner_id	")


class Chain(LLMBaseModel):
    intput: Optional[str] = Field(description="input value", examples="Who Are You!")
    output: Optional[str] = Field(description="output value", examples="I am ChatBot")

    def _get_type(self) -> str:
        return AliyunSpanKindValues.CHAIN.value

    def _get_attributes(self) -> dict:
        attributes = {}
        add_attribute(attributes, SpanAttributes.GEN_AI_SPAN_KIND, AliyunSpanKindValues.CHAIN.value)
        add_attribute(attributes, SpanAttributes.INPUT_VALUE, self.intput)
        add_attribute(attributes, SpanAttributes.OUTPUT_VALUE, self.output)
        return attributes


class Document(BaseModel):
    id: Optional[str] = Field(description="Unique identifier for a document",
                              examples="2aeab544-f93a-4477-b51d-bec27351325b")
    score: Optional[float] = Field(description="Score representing the relevance of a document", examples=0.98)
    content: Optional[str] = Field(description="The content of a retrieved document",
                                   examples="This is a sample document content.")
    metadata: Optional[dict] = Field(default=None,
                                     description="Metadata associated with a document",
                                     examples="{“file_path”: “data.txt”,}")


class ReRanker(LLMBaseModel):
    query: Optional[str] = Field(default=None,
                                 description="Query parameter of the reranker", examples="How to format timestamp?")
    rerank_model_name: Optional[str] = Field(default=None,
                                             description="Model name of the reranker",
                                             examples="cross-encoder/ms-marco-MiniLM-L-12-v2")
    top_k: Optional[int] = Field(default=None,
                                 description="Top K parameter of the reranker	", examples=3)
    input_documents: Optional[List[Document]] = Field(description="Input documents")
    output_documents: Optional[List[Document]] = Field(description="Output documents")

    def _get_type(self) -> str:
        return AliyunSpanKindValues.RERANKER.value

    def _get_attributes(self) -> dict:
        attributes = {}
        add_attribute(attributes, RerankerAttributes.RERANKER_QUERY, self.query)
        add_attribute(attributes, RerankerAttributes.RERANKER_MODEL_NAME, self.rerank_model_name)
        add_attribute(attributes, RerankerAttributes.RERANKER_TOP_K, self.top_k)
        idx = 0
        for document in self.input_documents:
            id_key = f"{RerankerAttributes.RERANKER_INPUT_DOCUMENTS}.{idx}.{DocumentAttributes.DOCUMENT_ID}"
            add_attribute(attributes, id_key, document.id)
            score_key = f"{RerankerAttributes.RERANKER_INPUT_DOCUMENTS}.{idx}.{DocumentAttributes.DOCUMENT_SCORE}"
            add_attribute(attributes, score_key, document.score)
            content_key = f"{RerankerAttributes.RERANKER_INPUT_DOCUMENTS}.{idx}.{DocumentAttributes.DOCUMENT_CONTENT}"
            add_attribute(attributes, content_key, document.content)
            metadata_key = f"{RerankerAttributes.RERANKER_INPUT_DOCUMENTS}.{idx}.{DocumentAttributes.DOCUMENT_METADATA}"
            add_attribute(attributes, metadata_key, document.metadata)
            idx = idx + 1
        idx = 0
        for document in self.output_documents:
            id_key = f"{RerankerAttributes.RERANKER_OUTPUT_DOCUMENTS}.{idx}.{DocumentAttributes.DOCUMENT_ID}"
            add_attribute(attributes, id_key, document.id)
            score_key = f"{RerankerAttributes.RERANKER_OUTPUT_DOCUMENTS}.{idx}.{DocumentAttributes.DOCUMENT_SCORE}"
            add_attribute(attributes, score_key, document.score)
            content_key = f"{RerankerAttributes.RERANKER_OUTPUT_DOCUMENTS}.{idx}.{DocumentAttributes.DOCUMENT_CONTENT}"
            add_attribute(attributes, content_key, document.content)
            metadata_key = f"{RerankerAttributes.RERANKER_OUTPUT_DOCUMENTS}.{idx}.{DocumentAttributes.DOCUMENT_METADATA}"
            add_attribute(attributes, metadata_key, document.metadata)
            idx = idx + 1
        return attributes


class Retriever(LLMBaseModel):
    documents: Optional[List[Document]] = Field(description="list of retriever document")

    def _get_type(self) -> str:
        return AliyunSpanKindValues.RETRIEVER.value

    def _get_attributes(self) -> dict:
        attributes = {}
        attributes[SpanAttributes.GEN_AI_SPAN_KIND] = AliyunSpanKindValues.RETRIEVER.value
        idx = 0
        for document in self.documents:
            id_key = f"{SpanAttributes.RETRIEVAL_DOCUMENTS}.{idx}.{DocumentAttributes.DOCUMENT_ID}"
            attributes[id_key] = document.id
            add_attribute(attributes, id_key, document.id)
            score_key = f"{SpanAttributes.RETRIEVAL_DOCUMENTS}.{idx}.{DocumentAttributes.DOCUMENT_SCORE}"
            add_attribute(attributes, id_key, document.score)
            content_key = f"{SpanAttributes.RETRIEVAL_DOCUMENTS}.{idx}.{DocumentAttributes.DOCUMENT_CONTENT}"
            add_attribute(attributes, content_key, document.content)
            metadata_key = f"{SpanAttributes.RETRIEVAL_DOCUMENTS}.{idx}.{DocumentAttributes.DOCUMENT_METADATA}"
            add_attribute(attributes, metadata_key, document.metadata)
            idx = idx + 1
        return attributes


class PromptTemplate(BaseModel):
    template: Optional[str] = Field(default=None,
                                    description="prompt template", examples="Weather forecast for {city} on {date}")
    variables: Optional[str] = Field(default=None,
                                     description="prompt variables",
                                     examples="{ context: \"<context from retrieval>\", subject: \"math\" }")
    version: Optional[str] = Field(default=None,
                                   description="prompt variables", examples="1.0")


class LLMRequest(BaseModel):
    parameters: Optional[str] = Field(description="request parameters",
                                      examples="a,b,c")
    llm_model_name: Optional[str] = Field(description="The name of the LLM a request is being made to",
                                          examples="gpt-4")
    max_tokens: Optional[int] = Field(default=None,
                                      description="The maximum number of tokens the LLM generates for a request.",
                                      examples=100)
    temperature: Optional[float] = Field(default=None,
                                         description="The temperature setting for the LLM request.", examples=0.1)
    top_p: Optional[float] = Field(default=None,
                                   description="The top_p sampling setting for the LLM request.	", examples=1)
    is_stream: Optional[bool] = Field(default=None,
                                      description="Whether the LLM responds with a stream.	", examples=True)
    stop_sequences: Optional[str] = Field(default=None,
                                          description="Array of strings the LLM uses as a stop sequence.",
                                          examples="[\"stop>\"]")
    tool_calls: Optional[str] = Field(default=None,
                                      description="List of tool calls (e.g. function calls)	",
                                      examples="[{\"tool_call.function.name\": \"get_current_weather\"}]")


class LLMResponse(BaseModel):
    llm_model_name: Optional[str] = Field(default=None,
                                          description="The name of the LLM a response was generated from.",
                                          examples="gpt-4-0613")
    finish_reason: Optional[str] = Field(default=None,
                                         description="Array of reasons the model stopped generating tokens, corresponding to each generation received.",
                                         examples="[\"stop\"]")
    first_token_duration: Optional[int] = Field(default=None, description="First packet latency, in nanoseconds",
                                                examples=100000)


class Usage(BaseModel):
    prompt_tokens: Optional[int] = Field(default=None,
                                         description="The number of tokens in the prompt")
    completion_tokens: Optional[int] = Field(default=None,
                                             description="The number of tokens in the completion")
    total_tokens: Optional[int] = Field(default=None,
                                        description="Total number of tokens, including prompt and completion	")
    image_input_tokens: Optional[int] = Field(default=None,
                                        description="The number of image input tokens	")
    audio_input_tokens: Optional[int] = Field(default=None,
                                        description="The number of audio input tokens	")
    vedio_input_tokens: Optional[int] = Field(default=None,
                                        description="The number of vedio input tokens	")


class ToolCall(BaseModel):
    function_name: Optional[str] = Field(default=None,
                                         description="tool function name")
    function_arguments: Optional[str] = Field(default=None,
                                              description="function argument")


class Message(BaseModel):
    role: Optional[str] = Field(default=None,
                                description="message role")
    content: Optional[str] = Field(default=None,
                                   description="message content")

    tool_calls: Optional[List[ToolCall]] = Field(default=None,
                                                 description="message content")


class LLMPrompt(BaseModel):
    content: Optional[str] = Field(default=None,
                                   description="content")
    message: Optional[Message] = Field(default=None,
                                       description="message info")


class LLMCompletion(BaseModel):
    content: Optional[str] = Field(default=None,
                                   description="completion content")
    message: Optional[Message] = Field(default=None,
                                       description="message info")


class LLM(LLMBaseModel):
    sub_kind: Optional[str] = Field(default=None,
                                    description="llm sub kind", examples="CHAT, COMPLETION")
    llm_model_name: Optional[str] = Field(default=None,
                                          description="request model name")
    input: Optional[str] = Field(description="input info", examples="Who Are You!")
    output: Optional[str] = Field(description="output info", examples="I am ChatBot")
    time_to_first_token: Optional[int] = Field(default=None, description="first token duration", examples=10)
    prompt_template: Optional[PromptTemplate] = Field(default=None,
                                                      description="prompt template")
    request: Optional[LLMRequest] = Field(default=None,
                                          description="request info")
    response: Optional[LLMResponse] = Field(default=None,
                                            description="response info")

    usage: Optional[Usage] = Field(default=None,
                                   description="llm usage")
    prompts_messages: Optional[List[Message]] = Field(description="prompts llm messages")

    completions_messages: Optional[List[Message]] = Field(description="completions llm messages")

    def _get_type(self) -> str:
        return AliyunSpanKindValues.LLM.value

    def _get_attributes(self) -> dict:
        attributes = {}
        add_attribute(attributes, SpanAttributes.GEN_AI_SPAN_KIND, self.get_type())
        add_attribute(attributes, SpanAttributes.GEN_AI_SPAN_SUB_KIND, self.sub_kind)
        add_attribute(attributes, SpanAttributes.GEN_AI_MODEL_NAME, self.llm_model_name)
        add_attribute(attributes, SpanAttributes.GEN_AI_USAGE_TOTAL_TOKENS, self.usage.total_tokens)
        add_attribute(attributes, SpanAttributes.GEN_AI_USAGE_PROMPT_TOKENS, self.usage.prompt_tokens)
        add_attribute(attributes, SpanAttributes.GEN_AI_USAGE_COMPLETION_TOKENS, self.usage.completion_tokens)
        add_attribute(attributes, "gen_ai.usage.image_input_tokens", self.usage.image_input_tokens)
        add_attribute(attributes, "gen_ai.usage.audio_input_tokens", self.usage.audio_input_tokens)
        add_attribute(attributes, "gen_ai.usage.vedio_input_tokens", self.usage.vedio_input_tokens)
        add_attribute(attributes, SpanAttributes.INPUT_VALUE, self.input)
        add_attribute(attributes, SpanAttributes.OUTPUT_VALUE, self.output)
        add_attribute(attributes, SpanAttributes.GEN_AI_REQUEST_TEMPERATURE, self.request.temperature)
        add_attribute(attributes, SpanAttributes.GEN_AI_REQUEST_TOP_P, self.request.top_p)
        add_attribute(attributes, SpanAttributes.GEN_AI_REQUEST_MAX_TOKENS, self.request.max_tokens)
        add_attribute(attributes, SpanAttributes.GEN_AI_REQUEST_IS_STREAM, self.request.is_stream)
        add_attribute(attributes, SpanAttributes.GEN_AI_REQUEST_MODEL_NAME, self.request.llm_model_name)
        add_attribute(attributes, SpanAttributes.GEN_AI_REQUEST_STOP_SEQUENCES, self.request.stop_sequences)
        add_attribute(attributes, SpanAttributes.GEN_AI_REQUEST_TOOL_CALLS, self.request.tool_calls)
        add_attribute(attributes, SpanAttributes.GEN_AI_REQUEST_PARAMETERS, self.request.parameters)
        add_attribute(attributes, SpanAttributes.GEN_AI_RESPONSE_FINISH_REASON, self.response.finish_reason)
        add_attribute(attributes, SpanAttributes.GEN_AI_RESPONSE_MODEL_NAME, self.response.llm_model_name)
        add_attribute(attributes, "gen_ai.response.time_to_first_token", self.time_to_first_token)
        if self.prompt_template is not None:
            add_attribute(attributes, SpanAttributes.GEN_AI_PROMPT_TEMPLATE, self.prompt_template.template)
            add_attribute(attributes, SpanAttributes.GEN_AI_PROMPT_VARIABLES, self.prompt_template.variables)
            add_attribute(attributes, SpanAttributes.GEN_AI_PROMPT_VERSION, self.prompt_template.version)
        for idx, message in enumerate(self.prompts_messages):
            role_key = f"{SpanAttributes.GEN_AI_PROMPT}.{idx}.{MessageAttributes.MESSAGE_ROLE}"
            add_attribute(attributes, role_key, message.role)
            content_key = f"{SpanAttributes.GEN_AI_PROMPT}.{idx}.{MessageAttributes.MESSAGE_CONTENT}"
            add_attribute(attributes, content_key, message.content)

        for idx, message in enumerate(self.completions_messages):
            role_key = f"{SpanAttributes.GEN_AI_COMPLETION}.{idx}.{MessageAttributes.MESSAGE_ROLE}"
            add_attribute(attributes, role_key, message.role)
            content_key = f"{SpanAttributes.GEN_AI_COMPLETION}.{idx}.{MessageAttributes.MESSAGE_CONTENT}"
            add_attribute(attributes, content_key, message.content)

        return attributes


class EmbeddingItem(BaseModel):
    text: Optional[str] = Field(None,
                                description="embedding text", examples="hello world")
    vector: Optional[str] = Field(None,
                                  description="embedding vector", examples="[0.123, 0.456, ...]")
    vector_size: Optional[int] = Field(None,
                                       description="embedding vector size", examples=1536)


if __name__ == "__main__":
    EmbeddingItem(text="hello world")


class Embeddings(LLMBaseModel):
    embedding_model_name: Optional[str] = Field(description="embedding model name", examples="EMBEDDING")
    prompt_tokens: Optional[int] = Field(None,
                                         description="prompt token / input token", examples=10)
    total_tokens: Optional[int] = Field(None,
                                        description="total token", examples=10)
    embedings: Optional[List[EmbeddingItem]] = Field([],
                                                     description="embedding list")

    def _get_type(self) -> str:
        return AliyunSpanKindValues.LLM.value

    def _get_attributes(self) -> dict:
        attributes = {}
        add_attribute(attributes, SpanAttributes.GEN_AI_SPAN_KIND, AliyunSpanKindValues.EMBEDDING.value)
        add_attribute(attributes, SpanAttributes.EMBEDDING_MODEL_NAME, self.embedding_model_name)
        add_attribute(attributes, SpanAttributes.GEN_AI_MODEL_NAME, self.embedding_model_name)
        add_attribute(attributes, SpanAttributes.GEN_AI_USAGE_PROMPT_TOKENS, self.prompt_tokens)
        add_attribute(attributes, SpanAttributes.GEN_AI_USAGE_TOTAL_TOKENS, self.total_tokens)
        for idx, embeding in enumerate(self.embedings):
            text_key = f"{SpanAttributes.EMBEDDING_EMBEDDINGS}.{idx}.{EmbeddingAttributes.EMBEDDING_TEXT}"
            add_attribute(attributes, text_key, embeding.text)
            vector_key = f"{SpanAttributes.EMBEDDING_EMBEDDINGS}.{idx}.{EmbeddingAttributes.EMBEDDING_VECTOR}"
            add_attribute(attributes, vector_key, embeding.vector)
            vector_size_key = f"{SpanAttributes.EMBEDDING_EMBEDDINGS}.{idx}.{EmbeddingAttributes.EMBEDDING_VECTOR_SIZE}"
            add_attribute(attributes, vector_size_key, embeding.vector_size)
        return attributes


class Task(LLMBaseModel):
    input: Optional[str] = Field(default=None,
                                 description="task input value")
    input_mime_type: Optional[str] = Field(default=None,
                                           description=["text/plain" "application/json"])
    output: Optional[str] = Field(default=None, description="task output value")

    output_mime_type: Optional[str] = Field(default=None, description=["text/plain" "application/json"])

    def _get_type(self) -> str:
        return "Task"

    def _get_attributes(self) -> dict:
        attributes = {}
        add_attribute(attributes)


class Tool(LLMBaseModel):
    name: Optional[str] = Field(description="tool name", examples="WeatherAPI")
    description: Optional[str] = Field(description="tool description", examples="An API to get weather data.")
    parameters: Optional[str] = Field(description="tool parameters", examples="{'a': 'int' }")
    input: Optional[str] = Field(default=None, description="input value", examples="who are you？")
    input_mime_type: Optional[str] = Field(default=None, description="tool parameters", examples="{'a': 'int' }")
    output: Optional[str] = Field(default=None, description="output value", examples="规划结束，请查看结果xxx")
    output_mime_type: Optional[str] = Field(None,
                                            description="output mime type")

    def _get_type(self) -> str:
        return AliyunSpanKindValues.TOOL.value

    def _get_attributes(self) -> dict:
        attributes = {}
        add_attribute(attributes, SpanAttributes.GEN_AI_SPAN_KIND, AliyunSpanKindValues.TOOL.value)
        add_attribute(attributes, SpanAttributes.TOOL_NAME, self.name)
        add_attribute(attributes, SpanAttributes.TOOL_DESCRIPTION, self.description)
        add_attribute(attributes, SpanAttributes.TOOL_PARAMETERS, self.parameters)
        add_attribute(attributes, SpanAttributes.INPUT_VALUE, self.input)
        add_attribute(attributes, SpanAttributes.INPUT_MIME_TYPE, self.input_mime_type)
        add_attribute(attributes, SpanAttributes.OUTPUT_VALUE, self.output)
        add_attribute(attributes, SpanAttributes.OUTPUT_MIME_TYPE, self.output_mime_type)
        return attributes


class Agent(LLMBaseModel):
    intput: Optional[str] = Field(description="agent input value", examples="请帮我规划xxxx!")
    input_mime_type: Optional[str] = Field(None,
                                           description="intput mime type")
    output: Optional[str] = Field(description="output value", examples="规划结束，请查看结果xxx")
    output_mime_type: Optional[str] = Field(None,
                                            description="output mime type")

    def _get_type(self) -> str:
        return AliyunSpanKindValues.AGENT.value

    def _get_attributes(self) -> dict:
        attributes = {}
        add_attribute(attributes, SpanAttributes.GEN_AI_SPAN_KIND, AliyunSpanKindValues.AGENT.value)
        add_attribute(attributes, SpanAttributes.INPUT_VALUE, self.intput)
        add_attribute(attributes, SpanAttributes.INPUT_MIME_TYPE, self.input_mime_type)
        add_attribute(attributes, SpanAttributes.OUTPUT_VALUE, self.output)
        add_attribute(attributes, SpanAttributes.OUTPUT_MIME_TYPE, self.output_mime_type)
        return attributes
