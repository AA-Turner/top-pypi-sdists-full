import attr


@attr.s(auto_attribs=True, frozen=True)
class CompletionPrompt:
    message: str
    suffix: str = ""
