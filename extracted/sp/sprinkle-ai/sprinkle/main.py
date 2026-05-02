import os
from dataclasses import dataclass
from typing import Callable, NoReturn, cast
from .parsing import Chunk, parse


@dataclass
class Args:
    verbose: bool
    output: bool
    editor: bool


def exec(text: str):
    os.execvp("bash", ["/usr/env/bash", "-c", text])


async def main(prompt: str, args: Args):
    from .inference import create_template
    from .tui import Sprinkle
    from .utils import merge
    import asyncio

    chunks, texts = parse(prompt)

    template = create_template()

    async def invoke(chunk: Chunk) -> Chunk:
        prompt_replaced = prompt.replace(chunk.text, "YOUR ANSWER IS HERE")
        out = await template.ainvoke({"chunk": chunk.text, "text": prompt_replaced})
        out = cast(str, out.content)
        if out[:1] == "'" and out[-1:] == "'":
            out = out[1:-1]
        if out[:1] == '"' and out[-1:] == '"':
            out = out[1:-1]
        res = Chunk.window(out, chunk.start, chunk.end)
        if args.verbose:
            print(f"searching for {chunk.text}, got {res.text}")
        return res

    contents = await asyncio.gather(*map(invoke, chunks))

    out = merge(contents, texts, chunk_comparer)
    out = " ".join(o.text for o in out)
    if args.verbose:
        print(f"executing 'bash /usr/env/bash -c {out}")

    action = print if args.output else exec

    result = out

    if args.editor:
        app = Sprinkle(out, cast(Callable[[str, Sprinkle], NoReturn], action))
        result = cast(str | None, await app.run_async())

    if result is not None:
        action(result)


def chunk_comparer(a: Chunk, b: Chunk) -> int:
    return b.start - a.start


def cli():
    """Command line interface for sprinkle."""
    import argparse
    import os
    import sys

    parser = argparse.ArgumentParser(description="AI-powered bash command generator")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="enable verbose output"
    )
    parser.add_argument(
        "-o", "--output", action="store_true", help="output to stdout instead of exec"
    )
    parser.add_argument(
        "-e",
        "--editor",
        action="store_true",
        help="edit the generated script before executing",
    )

    parser.add_argument(
        "prompt", nargs="*", help="natural language description of the command"
    )

    args = parser.parse_args()

    if "GOOGLE_API_KEY" not in os.environ:
        print(
            "\033[91mmissing google genai (gemini) api key. Please set GOOGLE_API_KEY environment variable with a valid gemini api key\033[0",
            file=sys.stderr,
        )
        exit(1)

    prompt = " ".join(args.prompt)
    if len(prompt) == 0:
        print("\033[91mno prompt was provided.\033[0", file=sys.stderr)
        exit(1)

    if args.verbose:
        print(f"Processing prompt: {prompt}", file=sys.stderr)

    if "{{" in prompt and "}}" in prompt:
        import asyncio

        asyncio.run(main(prompt, cast(Args, args)))
    else:
        exec(prompt)


if __name__ == "__main__":
    cli()
