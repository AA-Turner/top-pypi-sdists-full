import attr


@attr.s(auto_attribs=True, frozen=True)
class CompletionPrompt:
    prefix: str
    suffix: str = ""
