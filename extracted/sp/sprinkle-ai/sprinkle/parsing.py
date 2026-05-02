from dataclasses import dataclass


@dataclass
class Chunk:
    text: str
    start: int
    end: int

    @staticmethod
    def clip(text: str, start: int, end: int) -> "Chunk":
        return Chunk(text[start:end], start, end)

    @staticmethod
    def window(text: str, start: int = 0, end: int | None = None) -> "Chunk":
        if not end:
            end = len(text)
        return Chunk(text, start, end)


def chunk_comparer(a: Chunk, b: Chunk) -> int:
    return b.start - a.start


def parse(prompt: str) -> tuple[list[Chunk], list[Chunk]]:
    chunks: list[Chunk] = []
    start = prompt.find("{{")
    while 0 <= start < len(prompt):
        end = prompt.find("}}", start)
        if end < 0:
            break
        chunks.append(Chunk(prompt[start : end + 2], start, end + 2))
        start = prompt.find("{{", end)

    if not chunks:
        return [], [Chunk.window(prompt)]

    texts: list[Chunk] = []
    if chunks[0].start > 0:
        texts.append(Chunk.clip(prompt, 0, chunks[0].start))
    for p, n in zip(chunks, chunks[1:]):
        texts.append(Chunk.clip(prompt, p.end, n.start))
    if chunks[-1].end < len(prompt):
        texts.append(Chunk.clip(prompt, chunks[-1].end, len(prompt)))

    return chunks, texts
