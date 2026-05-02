from typing import Any, Callable, Coroutine, NoReturn
from textual.app import App, ComposeResult
from textual.widgets import Header, TextArea
from textual import events

Awaitable = Coroutine[Any, Any, None]


class Sprinkle(App):
    _on_finish_editing: Callable[[str, "Sprinkle"], NoReturn]

    @property
    def text(self):
        return self.query_one(OneLineTextArea).text

    def __init__(
        self,
        text: str,
        on_finish_editing: Callable[[str, "Sprinkle"], NoReturn],
    ):
        super().__init__()
        self._input_text = text
        self._on_finish_editing = on_finish_editing

    async def on_key(self, event: events.Key) -> None:
        if event.key == "enter":
            text = self.query_one(OneLineTextArea).text
            # release control of the terminal without exiting the process
            self.exit(text)

    def compose(self) -> ComposeResult:
        yield OneLineTextArea(self._input_text, self.on_key)


class OneLineTextArea(TextArea):
    on_return_key: Callable[[events.Key], Awaitable]

    def __init__(self, text: str, on_return_key: Callable[[events.Key], Awaitable]):
        super().__init__(text, compact=True)
        self.__on_return_key = on_return_key

    async def _on_key(self, event: events.Key) -> None:
        if event.key == "enter":
            await self.__on_return_key(event)
            event.prevent_default()
            event.stop()
        else:
            await super()._on_key(event)
