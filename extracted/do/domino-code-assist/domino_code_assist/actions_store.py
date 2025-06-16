import threading
from dataclasses import dataclass, field, replace
from enum import Enum
from typing import Any, List, Optional, Tuple

import reacton

from domino_code_assist.action import Action, ActionUseNbLocals, render_code_chunks
from domino_code_assist.assistant import mixpanel

e_insert_index = "insert_index"
e_edit_index = "edit_index"
e_delete_index = "delete_index"
e_insert_action = "insert_action"
e_edit_action = "edit_action"
e_undo = "undo"
e_redo = "redo"
e_reset = "reset"


@dataclass(frozen=True)
class DfWrapper:
    df: Any = field(repr=False, hash=None, compare=False, default_factory=lambda: None)
    actions: Optional[Tuple[Action]] = None

    @property
    def columns(self):
        if self.df is None:
            return None
        return tuple(self.df.columns.tolist()) if self.has_df else None

    @property
    def has_df(self):
        return self.df is not None


class ThreadState(Enum):
    RUNNING = 1
    CANCELLED = 2
    DONE = 3


@dataclass(frozen=True)
class ActionsState:
    df_wrapper: DfWrapper = DfWrapper()
    df_exec_status: ThreadState = ThreadState.DONE

    actions: List[Action] = field(default_factory=lambda: [])
    code_chunks: List[str] = field(default_factory=lambda: [])
    columns_for_action: List[List[str]] = field(default_factory=lambda: [])
    dtypes_for_action: List[List[str]] = field(default_factory=lambda: [])

    error: Optional[Tuple[int, str]] = None
    index_of_edit_action: Optional[int] = None
    index_of_insert_action: Optional[int] = None

    undo_stack: List[List[Action]] = field(default_factory=lambda: [])
    redo_stack: List[List[Action]] = field(default_factory=lambda: [])
    preview: bool = False


def actions_reducer(state: ActionsState, event) -> ActionsState:
    event_type, payload = event
    # print("reducer", state, event_type, payload)

    if event_type == e_insert_index:
        return replace(state, index_of_insert_action=payload)

    if event_type == e_edit_index:
        return replace(state, index_of_edit_action=payload)

    if event_type == e_insert_action:
        if isinstance(payload, Action):
            index = state.index_of_insert_action
        else:
            index = payload[0]
            payload = payload[1]

        if index is None:
            _actions = state.actions + [payload]
            mixpanel.api.track_with_defaults(
                "interaction",
                {
                    "section": "transformations",
                    "type": "add",
                    "transformation_type": type(payload).__name__,
                },
            )
        else:
            _actions = state.actions[: index + 1] + [payload] + state.actions[index + 1 :]
            mixpanel.api.track_with_defaults(
                "interaction",
                {
                    "section": "transformations",
                    "type": "insert",
                    "transformation_type": type(payload).__name__,
                },
            )
        return replace(state, undo_stack=state.undo_stack + [state.actions], redo_stack=[], actions=_actions, index_of_insert_action=None)

    if event_type == e_edit_action:
        index = state.index_of_edit_action
        if index is None:
            return state
        mixpanel.api.track_with_defaults(
            "interaction",
            {
                "section": "transformations",
                "type": "edit",
                "transformation_type": type(payload).__name__,
            },
        )
        return replace(
            state,
            undo_stack=state.undo_stack + [state.actions],
            redo_stack=[],
            actions=state.actions[:index] + [payload] + state.actions[index + 1 :],
            index_of_edit_action=None,
        )

    if event_type == e_delete_index:
        index = payload
        if index is None:
            return state
        mixpanel.api.track_with_defaults(
            "interaction",
            {"section": "transformations", "type": "delete", "transformation_type": type(state.actions[index]).__name__},
        )
        return replace(state, undo_stack=state.undo_stack + [state.actions], redo_stack=[], actions=state.actions[:index] + state.actions[index + 1 :])

    if event_type == e_undo:
        mixpanel.api.track_with_defaults(
            "interaction",
            {
                "section": "transformations",
                "type": "undo",
            },
        )
        return replace(state, actions=state.undo_stack[-1], undo_stack=state.undo_stack[:-1], redo_stack=state.redo_stack + [state.actions])

    if event_type == e_redo:
        item = state.redo_stack[-1]
        mixpanel.api.track_with_defaults(
            "interaction",
            {
                "section": "transformations",
                "type": "redo",
            },
        )
        return replace(state, actions=item, redo_stack=state.redo_stack[:-1], undo_stack=state.undo_stack + [state.actions])

    if event_type == e_reset:
        return ActionsState()

    return state


def use_execute_df(state: ActionsState, set_state, nb_locals=None):
    def execute():
        def run():
            chunks = render_code_chunks(state.actions)
            set_state(
                lambda state: replace(
                    state,
                    df_exec_status=ThreadState.RUNNING,
                    code_chunks=chunks,
                    error=None,
                )
            )
            error = None
            df = None
            try:
                columns_for_action = []
                dtypes_for_action = []
                scope = {**nb_locals} if nb_locals else {}
                if nb_locals and not state.preview:
                    scope = nb_locals
                actions = state.actions
                if state.actions and isinstance(state.actions[0], ActionUseNbLocals):
                    df = scope[actions[0].df_var_out]
                    actions = actions[1:]
                    columns_for_action = [df.columns.values.tolist()]
                    dtypes_for_action = [{k: v.name for k, v in df.dtypes.items()}]
                for index, (action, chunk) in enumerate(zip(actions, chunks)):
                    if chunk:
                        exec(chunk, scope)
                    df = scope[action.df_var_out]
                    columns_for_action.append(df.columns.values.tolist())
                    dtypes_for_action.append({k: v.name for k, v in df.dtypes.items()})
            except Exception as e:
                error = (index, str(e))

            set_state(
                lambda state: replace(
                    state,
                    df_wrapper=DfWrapper(df, actions=state.actions),
                    error=error,
                    columns_for_action=columns_for_action,
                    dtypes_for_action=dtypes_for_action,
                    df_exec_status=ThreadState.DONE,
                )
            )

        if not state.actions:
            set_state(lambda state: replace(state, df_wrapper=DfWrapper(), error=None, columns_for_action=[], code_chunks=[]))
            return

        threading.Thread(target=run).start()

    reacton.use_effect(execute, [state.actions])


def to_json(obj):
    if isinstance(obj, ActionsState):
        return {
            "type_action_state": {
                "actions": obj.actions,
                "undo_stack": obj.undo_stack,
                "redo_stack": obj.redo_stack,
                "preview": obj.preview,
            }
        }


def from_json(dct):
    if "type_action_state" in dct:
        dct = dct["type_action_state"]
        return ActionsState(**dct)
