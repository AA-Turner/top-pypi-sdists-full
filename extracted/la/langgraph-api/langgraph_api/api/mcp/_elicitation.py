from __future__ import annotations

import re
from collections import Counter
from contextlib import contextmanager
from dataclasses import dataclass, field, replace
from typing import TYPE_CHECKING, Literal, NoReturn, Protocol, TypeGuard
from urllib.parse import urlsplit

import jsonschema_rs
import mcp_types as types
import orjson
import structlog
from mcp.shared.exceptions import MCPError
from pydantic import TypeAdapter, ValidationError

from langgraph_api.api.mcp._constants import UNASKABLE_INPUT_MESSAGE
from langgraph_api.api.mcp._digest import digest
from langgraph_api.api.mcp._forms import FormSchema, FormTooLarge, UnsupportedSchema
from langgraph_api.api.mcp._origins import LOOPBACK_HOSTS
from langgraph_api.api.mcp._outcome import Failed

if TYPE_CHECKING:
    from collections.abc import Iterator, Mapping, Sequence

    from pydantic import JsonValue

    from langgraph_api.schema import Interrupt
    from langgraph_api.validation import SchemaValidator

logger = structlog.stdlib.get_logger(__name__)

TEXT_ANSWER: dict[str, JsonValue] = {"type": "string"}
ELICIT_PARAMS: TypeAdapter[types.ElicitRequestParams] = TypeAdapter(
    types.ElicitRequestParams
)
INTERRUPT_ID = re.compile(r"[0-9a-f]{32}")
MAX_URL_LENGTH = 4096
UNSAFE_URL = (
    "An elicitation URL needs https (or http on this machine), a host, "
    "and no credentials"
)
Refusal = Literal["decline", "cancel"]
Mode = Literal["form", "url"]
ENDED: dict[Refusal, str] = {"decline": "declined", "cancel": "cancelled"}
Results = dict[str, types.ElicitResult]
DECISION_TITLES: dict[str, str] = {
    "approve": "Approve",
    "edit": "Edit the arguments",
    "reject": "Reject",
    "respond": "Answer for the tool",
}
MESSAGE_DECISIONS = frozenset({"reject", "respond"})
REVIEW_MESSAGE: dict[str, JsonValue] = {
    "type": "string",
    "title": "Message",
    "description": "Why you reject the call, or the answer to send in its place",
}
REVIEW_ARGS: dict[str, JsonValue] = {
    "type": "string",
    "title": "Arguments",
    "description": "The arguments to run the tool with, as a JSON object",
}
DECISION_TYPE_PATH: list[str | int] = ["type"]
ANY_DECISION = jsonschema_rs.validator_for({})


class UnaskableInterrupt(ValueError):
    @property
    def outcome(self) -> Failed:
        return Failed(f"{UNASKABLE_INPUT_MESSAGE}: {self}")


class InvalidAnswer(MCPError):
    def __init__(self, message: str) -> None:
        super().__init__(types.INVALID_PARAMS, message)


@dataclass(frozen=True, slots=True)
class Resume:
    value: JsonValue

    @classmethod
    def single(cls, interrupt_id: str, value: JsonValue) -> Resume:
        if isinstance(value, dict) and all(map(INTERRUPT_ID.fullmatch, value)):
            return cls({interrupt_id: value})
        return cls(value)


@dataclass(frozen=True, slots=True)
class EndCall:
    refusal: Refusal

    @property
    def outcome(self) -> Failed:
        return Failed(f"The request for input was {ENDED[self.refusal]}.")


Reply = Resume | EndCall


@dataclass(frozen=True, slots=True)
class FormQuestion:
    key: str
    message: str
    form: FormSchema

    @property
    def mode(self) -> Mode:
        return "form"

    @property
    def request(self) -> types.ElicitRequest:
        return types.ElicitRequest(
            params=types.ElicitRequestFormParams(
                message=self.message, requested_schema=self.form.schema
            )
        )

    def answer(self, result: types.ElicitResult) -> JsonValue:
        return self.form.value(self._content(result))

    def relayed(self, result: types.ElicitResult) -> dict[str, JsonValue]:
        if result.action != "accept":
            return {"action": result.action}
        return {"action": "accept", "content": self._content(result)}

    def _content(self, result: types.ElicitResult) -> dict[str, JsonValue]:
        if (content := self.form.parse(result.content)) is None:
            raise InvalidAnswer("Form content does not match requestedSchema")
        return content


@dataclass(frozen=True, slots=True)
class UrlQuestion:
    key: str
    message: str
    url: str

    @property
    def mode(self) -> Mode:
        return "url"

    @property
    def request(self) -> types.ElicitRequest:
        return types.ElicitRequest(
            params=types.ElicitRequestURLParams(message=self.message, url=self.url)
        )

    def relayed(self, result: types.ElicitResult) -> dict[str, JsonValue]:
        return {"action": result.action}


Question = FormQuestion | UrlQuestion


class Prompt(Protocol):
    @property
    def questions(self) -> Sequence[Question]: ...

    def scoped(self, scope: str) -> Prompt: ...

    def refusal(self, results: Results) -> EndCall | None: ...

    def resume_value(self, results: Results) -> JsonValue: ...


@dataclass(frozen=True, slots=True)
class AnswerPrompt:
    question: FormQuestion

    @classmethod
    def of(cls, interrupt: Interrupt) -> AnswerPrompt:
        value = interrupt["value"]
        text = _text(value)
        schema = _answer_schema(text, interrupt.get("response_schema"))
        with _unaskable_schemas():
            form = FormSchema.wrapping(schema)
        message = text or orjson.dumps(value).decode()
        return cls(FormQuestion(f"answer-{digest(value, schema)}", message, form))

    @property
    def questions(self) -> tuple[FormQuestion]:
        return (self.question,)

    def scoped(self, scope: str) -> AnswerPrompt:
        return self

    def refusal(self, results: Results) -> EndCall | None:
        match results[self.question.key].action:
            case "decline" | "cancel" as refusal:
                return EndCall(refusal)
            case _:
                return None

    def resume_value(self, results: Results) -> JsonValue:
        return self.question.answer(results[self.question.key])


@dataclass(frozen=True, slots=True)
class RelayedRequests:
    requests: tuple[Question, ...]
    scope: str = ""

    @property
    def questions(self) -> tuple[Question, ...]:
        return tuple(
            replace(request, key=self.scope + request.key) for request in self.requests
        )

    def scoped(self, scope: str) -> RelayedRequests:
        return replace(self, scope=f"{scope}/")

    def refusal(self, results: Results) -> None:
        return None

    def resume_value(self, results: Results) -> JsonValue:
        return {
            "responses": {
                request.key: request.relayed(results[self.scope + request.key])
                for request in self.requests
            }
        }


@dataclass(frozen=True, slots=True)
class ReviewDialect:
    allowed_decisions: str
    edited_action: str

    def decisions_of(self, config: JsonValue) -> JsonValue:
        return config.get(self.allowed_decisions) if isinstance(config, dict) else None

    def edit(self, name: str, args: dict[str, JsonValue]) -> dict[str, JsonValue]:
        return {"type": "edit", self.edited_action: {"name": name, "args": args}}


SNAKE_CASE = ReviewDialect("allowed_decisions", "edited_action")
CAMEL_CASE = ReviewDialect("allowedDecisions", "editedAction")


@dataclass(slots=True)
class ReviewKeys:
    asked: Counter[str] = field(default_factory=Counter)

    def next(self, *action: JsonValue) -> str:
        reviewed = digest(*action)
        self.asked[reviewed] += 1
        return f"review-{reviewed}.{self.asked[reviewed]}"


@dataclass(frozen=True, slots=True)
class ReviewedAction:
    name: str
    decisions: tuple[str, ...]
    question: FormQuestion
    dialect: ReviewDialect

    @classmethod
    def of(
        cls,
        request: JsonValue,
        decisions: JsonValue,
        dialect: ReviewDialect,
        *,
        keys: ReviewKeys,
    ) -> ReviewedAction:
        match request:
            case {
                "name": str() as name,
                "args": dict() as args,
                **rest,
            } if _are_decisions(decisions):
                allowed = tuple(dict.fromkeys(decisions))
                message = _text(rest.get("description")) or f"Run {name}?"
                key = keys.next(name, args, message, allowed)
                question = FormQuestion(key, message, _review_form(args, allowed))
                return cls(name, allowed, question, dialect)
            case _:
                raise UnaskableInterrupt(
                    "A review needs a tool name, its arguments and its decisions"
                )

    def refusal(self, results: Results) -> EndCall | None:
        match results[self.question.key].action:
            case "cancel":
                return EndCall("cancel")
            case "decline" if "reject" not in self.decisions:
                return EndCall("decline")
            case _:
                return None

    def decision(self, results: Results) -> dict[str, JsonValue]:
        result = results[self.question.key]
        if result.action == "decline":
            return {"type": "reject"}
        return _decision(self.name, self.question.answer(result), self.dialect)


@dataclass(frozen=True, slots=True)
class ReviewPrompt:
    actions: tuple[ReviewedAction, ...]

    @classmethod
    def of(
        cls,
        requests: Sequence[JsonValue],
        configs: Sequence[JsonValue],
        dialect: ReviewDialect,
        *,
        keys: ReviewKeys,
    ) -> ReviewPrompt:
        if len(requests) != len(configs):
            raise UnaskableInterrupt("A review needs one review config per action")
        return cls(
            tuple(
                ReviewedAction.of(
                    request, dialect.decisions_of(config), dialect, keys=keys
                )
                for request, config in zip(requests, configs, strict=True)
            )
        )

    @property
    def questions(self) -> tuple[FormQuestion, ...]:
        return tuple(action.question for action in self.actions)

    def scoped(self, scope: str) -> ReviewPrompt:
        return self

    def refusal(self, results: Results) -> EndCall | None:
        for action in self.actions:
            if (refusal := action.refusal(results)) is not None:
                return refusal
        return None

    def resume_value(self, results: Results) -> JsonValue:
        return {"decisions": [action.decision(results) for action in self.actions]}


@dataclass(frozen=True, slots=True)
class DecisionSchema:
    schema: JsonValue

    def checked(self, decision: dict[str, JsonValue]) -> dict[str, JsonValue]:
        validator = _decision_validator(self.schema)
        try:
            validator.validate(decision)
        except jsonschema_rs.ValidationError as error:
            raise InvalidAnswer(
                f"The decision does not fit the tool: {_reason(error)}"
            ) from None
        return decision


@dataclass(frozen=True, slots=True)
class ToolApprovalPrompt:
    action: ReviewedAction
    schema: DecisionSchema

    @classmethod
    def of(
        cls, approval: JsonValue, schema: JsonValue, *, keys: ReviewKeys
    ) -> ToolApprovalPrompt:
        decisions = _approval_decisions(schema)
        action = ReviewedAction.of(approval, decisions, SNAKE_CASE, keys=keys)
        return cls(action, DecisionSchema(schema))

    @property
    def questions(self) -> tuple[FormQuestion]:
        return (self.action.question,)

    def scoped(self, scope: str) -> ToolApprovalPrompt:
        return self

    def refusal(self, results: Results) -> EndCall | None:
        return self.action.refusal(results)

    def resume_value(self, results: Results) -> JsonValue:
        return self.schema.checked(self.action.decision(results))


@dataclass(frozen=True, slots=True)
class Round:
    prompts: Mapping[str, Prompt]
    questions: Mapping[str, Question]

    @classmethod
    def of(cls, interrupts: Sequence[Interrupt]) -> Round:
        keys = ReviewKeys()
        prompts = {
            _interrupt_id(interrupt): _prompt(interrupt, keys)
            for interrupt in interrupts
        }
        if len(prompts) > 1:
            scopes = _scopes(interrupts)
            prompts = {
                interrupt_id: prompt.scoped(scopes[interrupt_id])
                for interrupt_id, prompt in prompts.items()
            }
        questions: dict[str, Question] = {}
        for prompt in prompts.values():
            for question in prompt.questions:
                if questions.setdefault(question.key, question) != question:
                    raise UnaskableInterrupt(
                        f"Two different questions use the key {question.key!r}"
                    )
        return cls(prompts, questions)

    @property
    def digest(self) -> str:
        return digest(
            {
                key: question.request.model_dump(mode="json", exclude_none=True)
                for key, question in self.questions.items()
            }
        )

    @property
    def modes(self) -> frozenset[Mode]:
        return frozenset(question.mode for question in self.questions.values())

    @property
    def input_requests(self) -> types.InputRequests:
        return {key: question.request for key, question in self.questions.items()}

    def answered_by(self, answers: Mapping[str, types.InputResponse]) -> bool:
        return self.questions.keys() <= answers.keys()

    def reply(self, answers: Mapping[str, types.InputResponse]) -> Reply:
        results = {key: _elicit_result(answers[key]) for key in self.questions}
        for prompt in self.prompts.values():
            if (refusal := prompt.refusal(results)) is not None:
                return refusal
        resumed = {
            interrupt_id: prompt.resume_value(results)
            for interrupt_id, prompt in self.prompts.items()
        }
        match list(resumed.items()):
            case [(interrupt_id, value)]:
                return Resume.single(interrupt_id, value)
            case _:
                return Resume(resumed)


def _prompt(interrupt: Interrupt, keys: ReviewKeys) -> Prompt:
    match interrupt["value"]:
        case {"type": "mcp_elicitation", "requests": [_, *_] as listed}:
            return RelayedRequests(tuple(map(_listed_question, listed)))
        case {"type": "mcp_elicitation", "requests": {**keyed}} if keyed:
            return RelayedRequests(
                tuple(_relayed_question(key, request) for key, request in keyed.items())
            )
        case {"type": "mcp_elicitation"}:
            raise UnaskableInterrupt("An mcp_elicitation interrupt needs a request")
        case {"type": "tool_approval"} as approval:
            schema = interrupt.get("response_schema")
            return ToolApprovalPrompt.of(approval, schema, keys=keys)
        case {
            "action_requests": [_, *_] as requests,
            "review_configs": list() as configs,
        }:
            return ReviewPrompt.of(requests, configs, SNAKE_CASE, keys=keys)
        case {
            "actionRequests": [_, *_] as requests,
            "reviewConfigs": list() as configs,
        }:
            return ReviewPrompt.of(requests, configs, CAMEL_CASE, keys=keys)
        case _:
            return AnswerPrompt.of(interrupt)


def _scopes(interrupts: Sequence[Interrupt]) -> dict[str, str]:
    asked: Counter[str] = Counter()
    scopes: dict[str, str] = {}
    for interrupt in interrupts:
        question = digest(interrupt["value"])
        asked[question] += 1
        scopes[_interrupt_id(interrupt)] = f"{question}.{asked[question]}"
    return scopes


def _listed_question(request: JsonValue) -> Question:
    key = request.get("key") if isinstance(request, dict) else None
    return _relayed_question(key, request)


def _relayed_question(key: JsonValue, request: JsonValue) -> Question:
    match key, _elicit_params(request):
        case str() as key, types.ElicitRequestFormParams(
            message=message, requested_schema=schema
        ) if key and _text(message):
            with _unaskable_schemas():
                return FormQuestion(key, message, FormSchema.of(schema))
        case str() as key, types.ElicitRequestURLParams(message=message, url=url) if (
            key and _text(message)
        ):
            return UrlQuestion(key, message, _safe_url(url))
        case _:
            raise UnaskableInterrupt(
                "An mcp_elicitation request needs a key, a message, "
                "and a form schema or a URL"
            )


def _elicit_params(request: JsonValue) -> types.ElicitRequestParams | None:
    try:
        return ELICIT_PARAMS.validate_python(request)
    except ValidationError:
        return None


def _are_decisions(values: JsonValue) -> TypeGuard[list[str]]:
    return (
        isinstance(values, list)
        and bool(values)
        and all(isinstance(value, str) and value in DECISION_TITLES for value in values)
    )


def _approval_decisions(schema: JsonValue) -> JsonValue:
    match schema:
        case {"discriminator": {"mapping": dict() as mapping}}:
            return list(mapping)
        case {"oneOf": [*branches]} | {"anyOf": [*branches]}:
            return [_decision_type(branch) for branch in branches]
        case _:
            return [_decision_type(schema)]


def _decision_type(branch: JsonValue) -> JsonValue:
    match branch:
        case {"properties": {"type": {"const": str() as decision}}}:
            return decision
        case _:
            return None


def _decision_validator(schema: JsonValue) -> SchemaValidator:
    try:
        return jsonschema_rs.validator_for(
            schema, retriever=_never_fetch, validate_formats=False
        )
    except jsonschema_rs.ValidationError as error:
        logger.warning(
            "A tool approval's response_schema does not compile, "
            "so this answer is not checked",
            error=error.message,
        )
        return ANY_DECISION


def _never_fetch(uri: str) -> NoReturn:
    raise ValueError(f"The server never fetches {uri}")


def _reason(error: jsonschema_rs.ValidationError) -> str:
    match error.kind:
        case (
            jsonschema_rs.ValidationErrorKind.OneOfNotValid(context=branches)
            | jsonschema_rs.ValidationErrorKind.AnyOf(context=branches)
        ):
            for errors in branches:
                if not _rejects_the_type(errors):
                    return errors[0].message
    return error.message


def _rejects_the_type(errors: list[jsonschema_rs.ValidationError]) -> bool:
    return any(error.instance_path == DECISION_TYPE_PATH for error in errors)


def _review_form(args: dict[str, JsonValue], decisions: tuple[str, ...]) -> FormSchema:
    with _unaskable_schemas():
        try:
            return FormSchema.of(_review_schema(args, decisions))
        except FormTooLarge:
            uneditable = tuple(decision for decision in decisions if decision != "edit")
            if not uneditable:
                raise
            return FormSchema.of(_review_schema(args, uneditable))


def _review_schema(
    args: dict[str, JsonValue], decisions: tuple[str, ...]
) -> dict[str, JsonValue]:
    choices = [
        {"const": decision, "title": DECISION_TITLES[decision]}
        for decision in decisions
    ]
    fields: dict[str, JsonValue] = {
        "decision": {"type": "string", "title": "Decision", "oneOf": choices}
    }
    if MESSAGE_DECISIONS.intersection(decisions):
        fields["message"] = REVIEW_MESSAGE
    if "edit" in decisions:
        fields["args"] = {**REVIEW_ARGS, "default": orjson.dumps(args).decode()}
    return {"type": "object", "properties": fields, "required": ["decision"]}


def _decision(
    name: str, answer: JsonValue, dialect: ReviewDialect
) -> dict[str, JsonValue]:
    match answer:
        case {"decision": "approve"}:
            return {"type": "approve"}
        case {"decision": "reject", **rest}:
            reason = _text(rest.get("message"))
            return (
                {"type": "reject", "message": reason} if reason else {"type": "reject"}
            )
        case {"decision": "respond", "message": str() as message} if _text(message):
            return {"type": "respond", "message": message}
        case {"decision": "edit", "args": str() as args}:
            return dialect.edit(name, _json_object(args))
        case _:
            raise InvalidAnswer("A decision needs its message or its arguments")


def _json_object(text: str) -> dict[str, JsonValue]:
    try:
        value = orjson.loads(text)
    except orjson.JSONDecodeError:
        value = None
    if not isinstance(value, dict):
        raise InvalidAnswer("Edited arguments must be a JSON object")
    return value


def _safe_url(url: str) -> str:
    try:
        parsed = urlsplit(url)
        port = parsed.port
    except ValueError:
        raise UnaskableInterrupt(UNSAFE_URL) from None
    secure = parsed.scheme == "https" or (
        parsed.scheme == "http" and parsed.hostname in LOOPBACK_HOSTS
    )
    if (
        not secure
        or not parsed.hostname
        or parsed.username is not None
        or port == 0
        or len(url) > MAX_URL_LENGTH
        or any(char.isspace() or not char.isprintable() for char in url)
    ):
        raise UnaskableInterrupt(UNSAFE_URL)
    return url


@contextmanager
def _unaskable_schemas() -> Iterator[None]:
    try:
        yield
    except UnsupportedSchema as error:
        raise UnaskableInterrupt(str(error)) from None


def _elicit_result(response: types.InputResponse) -> types.ElicitResult:
    if isinstance(response, types.ElicitResult):
        return response
    raise InvalidAnswer("Expected an elicitation result")


def _interrupt_id(interrupt: Interrupt) -> str:
    if interrupt_id := interrupt.get("id"):
        return interrupt_id
    raise UnaskableInterrupt("An interrupt without an id cannot be resumed")


def _text(value: JsonValue) -> str | None:
    return value if isinstance(value, str) and value.strip() else None


def _answer_schema(
    text: str | None, declared: dict[str, JsonValue] | None
) -> dict[str, JsonValue]:
    if isinstance(declared, dict) and declared:
        return declared
    if text is not None:
        return TEXT_ANSWER
    raise UnaskableInterrupt(
        "An interrupt that is not a text question needs a response_schema"
    )
