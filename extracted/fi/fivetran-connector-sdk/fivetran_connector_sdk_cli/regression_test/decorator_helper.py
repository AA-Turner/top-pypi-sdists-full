"""
The `@action` decorator of the open-source package, and what happens to an `@action` call during
`fivetran debug --record` and `fivetran debug --replay`: work out which arguments identify the call and mask
credentials. A recording then calls the live source and hands (name, arguments, result) to the Recorder; a replay
returns the matching recorded result from the Replayer without calling the source.

Production's package defines an `@action` of the same name that returns the function unchanged.
"""

import functools
import hashlib
import hmac
import inspect
import json
import re
from typing import Any, Callable, Dict, Optional

from fivetran_connector_sdk_cli.regression_test.fixture_helper import RecordError
from fivetran_connector_sdk_cli.regression_test.max_record_helper import MaxRecordHandler, MaxRecordsReached
from fivetran_connector_sdk_cli.regression_test.recorder import Recorder
from fivetran_connector_sdk_cli.regression_test.replayer import Replayer

# Argument names that look like credentials. This is a name-based heuristic: it
# can miss a secret under an innocuous name (for example nested inside a
# "headers" dict) and can flag a harmless field such as a pagination "page_token".
_SECRET_KEY_PATTERN = re.compile(r"(?:api[_-]?key|private[_-]?key|secret[_-]?key|access[_-]?key|token|secret|password|passwd|pwd|bearer|cookie|credential|configuration)s?$", re.IGNORECASE)

# Public, fixed pepper for the HMAC below. It only defends against generic
# precomputed tables; it cannot protect low-entropy secrets such as a short PIN.
_SECRET_HASH_PEPPER = b"fivetran-connector-sdk-record-replay-v1"

# Signatures of the functions whose `match=` has already been checked, so the check runs once per function.
_validated_signatures: Dict[Callable, inspect.Signature] = {}


def _looks_like_secret_key(key: str) -> bool:
    return _SECRET_KEY_PATTERN.search(key) is not None


def _mask_secret_args(matched_args: dict) -> dict:
    """
    Replace the value of every credential-looking argument with a tagged HMAC-SHA256 digest.

    Hashing, rather than dropping the key, keeps calls made with different secrets
    distinguishable while never writing the raw value to fixture.jsonl. The keys of nested dicts,
    including dicts inside lists and tuples, are checked too. It returns new dicts and lists, so the
    result is not affected if the source function later changes its arguments. Results are never masked.
    """
    masked = {}
    for key, value in matched_args.items():
        if isinstance(key, str) and _looks_like_secret_key(key):
            digest = hmac.new(
                _SECRET_HASH_PEPPER, str(value).encode("utf-8"), hashlib.sha256
            ).hexdigest()
            masked[key] = f"sha256:{digest}"
        else:
            masked[key] = _mask_nested(value)
    return masked


def _mask_nested(value: Any) -> Any:
    if isinstance(value, dict):
        return _mask_secret_args(value)
    if isinstance(value, (list, tuple)):
        return [_mask_nested(item) for item in value]
    return value


def _validate_match(name: str, func: Callable, sig: inspect.Signature, match: Optional[Callable]) -> None:
    """
    Check once that `match`, if given, can be called with the function's arguments.

    Raises TypeError if the function takes a variable number of arguments, or if `match`
    does not accept one value per parameter of the function.
    """
    if match is None:
        return
    if any(
        p.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD)
        for p in sig.parameters.values()
    ):
        raise TypeError(
            f"@action '{name}': match= cannot be used with '{func.__name__}' because it accepts "
            "a variable number of arguments. Declare each argument by name "
            "in the function, or remove match=."
        )
    try:
        inspect.signature(match).bind(*sig.parameters)
    except TypeError:
        raise TypeError(
            f"@action '{name}': match= must accept the same arguments as "
            f"{func.__name__} ({', '.join(sig.parameters)})."
        ) from None


def _compute_matched_args(name: str,
                          sig: inspect.Signature,
                          match: Optional[Callable],
                          args: tuple,
                          kwargs: dict) -> dict:
    """
    Return the dict that identifies this call in the fixture.

    Arguments are first bound to the function's signature (defaults applied), so
    the result is the same whether the caller passed them positionally or by keyword.
    With `match`, it is called with the resolved values positionally and must return a
    dict; otherwise the full {parameter name: value} dict is used.
    """
    bound = sig.bind(*args, **kwargs)
    bound.apply_defaults()

    if match is None:
        return dict(bound.arguments)

    matched_args = match(*bound.arguments.values())
    if not isinstance(matched_args, dict):
        raise TypeError(
            f"@action '{name}': match= must return a dict, got {type(matched_args).__name__}."
        )
    return matched_args


def _identify_call(name: str, func: Callable, match: Optional[Callable], args: tuple, kwargs: dict) -> dict:
    """Return the masked dict that identifies this call, the same way for recording and replay."""
    signature = _validated_signatures.get(func)
    if signature is None:
        signature = inspect.signature(func)
        _validate_match(name, func, signature, match)
        _validated_signatures[func] = signature
    return _mask_secret_args(_compute_matched_args(name, signature, match, args, kwargs))


def _json_round_trip(value: Any) -> Any:
    """The value as it looks after being saved to and loaded from the fixture (tuples become lists, keys strings)."""
    return json.loads(json.dumps(value, allow_nan=False))


def replay_action_call(name: str, func: Callable, match: Optional[Callable], args: tuple, kwargs: dict) -> Any:
    """Return the recorded result for this call without calling the live source."""
    return Replayer.lookup(name, _json_round_trip(_identify_call(name, func, match, args, kwargs)))


def _fixture_serialization_error(name: str, what: str, hint: str, cause: BaseException) -> RecordError:
    """The RecordError that names the action and why its argument or result cannot be written as JSON."""
    return RecordError(f"Interaction '{name}' has a {what} that cannot be recorded: {cause}. {hint}")


def record_action_call(name: str, func: Callable, match: Optional[Callable], args: tuple, kwargs: dict) -> Any:
    """Call the live source, store the interaction in the fixture and return the result as replay will return it."""
    identified = _identify_call(name, func, match, args, kwargs)
    try:
        matched_args = _json_round_trip(identified)
    except (TypeError, ValueError, RecursionError) as e:
        raise _fixture_serialization_error(
            name, "argument",
            "Use plain dicts, lists, strings, numbers, booleans or None, or supply a match= lambda "
            "that extracts only JSON-safe values from the arguments.", e) from e

    # A raising function records nothing: the error propagates, so the recording fails like a normal run would.
    result = func(*args, **kwargs)

    # The arguments were checked above, so an error here comes from the result; nothing is written when it fails.
    # The connector gets the saved-and-reloaded result, so it sees the same types during record and replay.
    try:
        Recorder.record(name, matched_args, result)
        return _json_round_trip(result)
    except (TypeError, ValueError, RecursionError) as e:
        raise _fixture_serialization_error(
            name, "result",
            "Return plain dicts, lists, strings, numbers, booleans or None from @action functions.", e) from e


_recording = False
_replaying = False


class DuplicateActionError(ValueError):
    """Two different functions use the same @action interaction name."""


# Interaction name -> {id(function): function}, filled when each @action is applied (at import). Nothing is
# raised there, so plain `fivetran debug` is unaffected; record and replay check it with check_unique_action_names().
_registered_actions: Dict[str, Dict[int, Callable]] = {}


def set_recording(enabled: bool) -> None:
    """Turn recording of @action calls on or off. Takes effect for every @action, including ones already defined."""
    global _recording
    _recording = enabled


def set_replaying(enabled: bool) -> None:
    """Turn replay of @action calls on or off: while on, @action functions return recorded results and never run."""
    global _replaying
    _replaying = enabled


def _describe(func: Callable) -> str:
    """Return 'qualname (file:line)' for a function, or just the qualname if the source is unavailable."""
    try:
        return f"{func.__qualname__} ({inspect.getsourcefile(func)}:{inspect.getsourcelines(func)[1]})"
    except (OSError, TypeError):
        return func.__qualname__


def _register_action(name: str, func: Callable) -> None:
    _registered_actions.setdefault(name, {})[id(func)] = func


def check_unique_action_names() -> None:
    """Raise DuplicateActionError if two different functions share an @action name."""
    for name, funcs in _registered_actions.items():
        if len(funcs) > 1:
            listing = "\n".join(f"  {_describe(func)}" for func in funcs.values())
            raise DuplicateActionError(
                f"@action interaction name '{name}' is used by two different functions:\n{listing}\n"
                "each @action interaction name must uniquely identify one function"
            )


def action(name: str, match: Optional[Callable] = None):
    """
    Mark a source-reading function for recording and replay.

        @action("customers_page", match=lambda cursor: {"cursor": cursor})
        def fetch_customers_page(cursor):
            ...

    Args:
        name:  Stable identifier for this call site, stored in the fixture. Reusing
               it for repeated calls to the same function (for example, paging with
               different cursors) is expected.
        match: Optional callable that receives the decorated function's resolved
               arguments positionally and returns the dict that identifies the
               call. If omitted, all bound arguments are used. For a method, `self` is one of those arguments and is
               not JSON-serializable, so `match` is required and must leave `self` out of the returned dict.

    The wrapper checks whether recording is on, see set_recording(), and likewise whether replay is on, see
    set_replaying(), each time it is called, so it works however early the connector module was imported.
    When both are off it just calls the function. While replaying, it returns the recorded result instead.

    Raises:
        DuplicateActionError: for a record or replay run (not plain `debug`) when `name` is used by a different
            function. Interaction names are the only thing that tells recorded calls apart, so a shared name
            would make them indistinguishable. Connector checks all names before the run starts.
    """
    def decorator(func: Callable) -> Callable:
        _register_action(name, func)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # After the --max-records cap ended the sync, a worker thread may still be running. Stop it here, so a
            # recording makes no more live source calls and a replay does not fail on calls the recording skipped.
            if (_recording or _replaying) and MaxRecordHandler.is_stopped_by_cap():
                raise MaxRecordsReached(
                    f"--max-records cap reached; skipping @action '{name}' call, the sync is already ending."
                )

            if _recording:
                return record_action_call(name, func, match, args, kwargs)

            if _replaying:
                return replay_action_call(name, func, match, args, kwargs)

            return func(*args, **kwargs)

        return wrapper
    return decorator
