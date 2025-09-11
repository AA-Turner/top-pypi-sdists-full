import os,re
from .read_write_utils import write_to_file
from .type_utils import make_list
from .class_utils import get_class_inputs
from .math_utils import find_common_denominator
from typing import List
import tiktoken
from dataclasses import dataclass,asdict
@dataclass
class ChunkParams:
    text: str
    max_tokens: int = 1000
    model_name: str = "gpt-4"
    encoding_name: str = None
    overlap: int = 0
    verbose: bool = False
    reverse: bool = False
def detect_language_from_text(text: str):
    patterns = {
        'javascript': [
            r'\bfunction\s+\w+\s*\(.*\)\s*{',
            r'\bvar\s+\w+\s*=',
            r'\bconst\s+\w+\s*=',
            r'\blet\s+\w+\s*=',
            r'\bconsole\.log\s*\(',
            r'\bexport\s+(default|function|const|class)',
            r'\bimport\s+.*\s+from\s+[\'"]'
        ],
        'typescript': [
            r'\binterface\s+\w+\s*{',
            r'\btype\s+\w+\s*=',
            r'\blet\s+\w+:\s+\w+',
            r'\bfunction\s+\w+\s*\(.*:\s*\w+\)',
            r'\bimport\s+.*\s+from\s+[\'"]',
            r'\bexport\s+(default|function|const|class)'
        ],
        'python': [
            r'\bdef\s+\w+\(',
            r'\bclass\s+\w+\s*:',
            r'\bimport\s+\w+',
            r'\bfrom\s+\w+\s+import\s+\w+',
            r'\bif\s+__name__\s*==\s*[\'"]__main__[\'"]',
            r'@\w+',
            r'\blambda\s+'
        ],
        'html': [
            r'<!DOCTYPE\s+html>',
            r'<html[^>]*>',
            r'<head>',
            r'<body>',
            r'<div[^>]*>',
            r'<script[^>]*>',
            r'</\w+>'
        ],
        'php': [
            r'<\?php',
            r'\$\w+\s*=',
            r'echo\s+["\']',
            r'->\w+\(',
            r'function\s+\w+\s*\(',
            r'\bclass\s+\w+\s*{'
        ],
        'bash': [
            r'#!/bin/bash',
            r'\becho\s+["\']',
            r'\bif\s+\[\[?',
            r'\bthen\b',
            r'\bfi\b',
            r'\bfor\s+\w+\s+in\b',
            r'\bdo\b',
            r'\bdone\b'
        ]
    }
    text = str(text)
    scores = {lang: sum(bool(re.search(p, text)) for p in pats) for lang, pats in patterns.items()}
    max_score = max(scores.values(), default=0)

    if max_score == 0:
        return 'neither'

    likely = [lang for lang, score in scores.items() if score == max_score]
    return likely[0] if len(likely) == 1 else 'uncertain'

def search_code(code_languages, parts):
    return [data for datas in parts for data in make_list(datas)
            if detect_language_from_text(data) in code_languages]
def get_token_encoder(model_name: str = "gpt-4", encoding_name: str = None):
    import tiktoken
    """
    Retrieves the encoder for a given model or encoding name.
    
    Args:
        model_name (str): The name of the model. Defaults to "gpt-4".
        encoding_name (str, optional): The encoding name to use. If not provided, it defaults based on the model.

    Returns:
        Encoder: A tiktoken encoder object.
    """
    if encoding_name:
        return tiktoken.get_encoding(encoding_name)
    else:
        return tiktoken.encoding_for_model(model_name)

def num_tokens_from_string(string: str, model_name: str = "gpt-4", encoding_name: str = None) -> int:
    """
    Returns the number of tokens in a text string.

    Args:
        string (str): The input text.
        model_name (str, optional): The model name to determine encoding if encoding_name is not specified. Defaults to "gpt-4".
        encoding_name (str, optional): The encoding name to use. If not specified, uses model-based encoding.

    Returns:
        int: The count of tokens.
    """
    encoding = get_token_encoder(model_name, encoding_name)
    num_tokens = len(encoding.encode(str(string)))
    return num_tokens

def infer_tab_size(file_path):
    if not os.path.isfile(file_path):
        write_to_file(file_path=file_path, contents='\t')
    with open(file_path, 'r') as file:
        for line in file:
            if '\t' in line:
                return len(line) - len(line.lstrip())  # The length of indentation
    return 4  # Default if no tab found

def get_blocks(data, delim='\n'):
    if isinstance(data, list):
        return data, None
    if isinstance(data, tuple):
        data, delim = data[0], data[-1]
    return data.split(delim), delim

def get_indent_levels(text):
    tab_size, indent_list = infer_tab_size('config.txt'), [0]
    for line in text.split('\n'):
        indent = 0
        for char in line:
            if char in [' ', '\t']:
                indent += tab_size if char == '\t' else 1
            else:
                break
        if indent not in indent_list:
            indent_list.append(indent)
    return indent_list

def get_code_blocks(data, indent_level=0):
    blocks = [[]]
    lines, delim = get_blocks(data, '\n')
    for line in lines:
        beginning = ''
        for char in line:
            if char in ['', ' ', '\n', '\t']:
                beginning += char
            else:
                break
        if len(beginning) == indent_level:
            blocks[-1] = delim.join(blocks[-1])
            blocks.append([line])
        else:
            blocks[-1].append(line)
    blocks[-1] = delim.join(blocks[-1])
    return blocks, delim

def chunk_any_to_tokens(data, max_tokens, model_name="gpt-4", encoding_name=None, delimiter='\n\n', reverse=False):
    if isinstance(data, list):
        blocks = data
    else:
        blocks, delimiter = get_blocks(data, delimiter)

    if reverse:
        blocks = reversed(blocks)

    chunks = []
    current_chunk = []

    for block in blocks:
        if num_tokens_from_string(delimiter.join(current_chunk + [block]), model_name, encoding_name) <= max_tokens:
            current_chunk.append(block)
        else:
            if current_chunk:
                chunks.append(delimiter.join(current_chunk))
            current_chunk = [block]

    if current_chunk:
        chunks.append(''.join(current_chunk))

    return chunks

def chunk_data_by_type(data, max_tokens, chunk_type=None, model_name="gpt-4", encoding_name=None, reverse=False):
    delimiter = None
    if chunk_type == "URL":
        delimiter = None
        blocks = re.split(r'<h[1-6].*?>.*?</h[1-6]>', data)
    elif chunk_type == "SOUP":
        delimiter = None
        blocks = data
    elif chunk_type == "DOCUMENT":
        delimiter = "."
        blocks = data.split(delimiter)
    elif chunk_type == "CODE":
        return chunk_source_code(data, max_tokens, model_name, encoding_name, reverse=reverse)
    elif chunk_type == "TEXT":
        return chunk_text_by_tokens(data, max_tokens, model_name, encoding_name, reverse=reverse)
    else:
        delimiter = "\n\n"
        blocks = data.split(delimiter)
    
    return chunk_any_to_tokens(blocks, max_tokens, model_name, encoding_name, delimiter, reverse=reverse)
def chunk_by_language_context(
    text: str,
    max_tokens: int = 1000,
    model_name: str = "gpt-4",
    encoding_name: str = None,
    overlap: int = 0,
    verbose: bool = False,
    reverse: bool = False
) -> List[str]:
    """
    Detects language and applies chunking strategy best suited to that context.
    """
    task_params = get_class_inputs(ChunkParams,
                             max_tokens=max_tokens,
                             model_name=model_name,
                             encoding_name=encoding_name,
                             overlap=overlap,
                             verbose=verbose,
                             reverse=reverse
                            )
    language = detect_language_from_text(text)
    
    if verbose:
        print(f"Detected language: {language}")

    if language == 'python':
        return chunk_source_code(text, task_params.max_tokens, task_params.model_name, task_params.encoding_name, task_params.reverse)

    elif language in n('js','typescript'):
        return chunk_by_braces(text, task_params.max_tokens, task_params.model_name, task_params.encoding_name, open='{', close='}', verbose=task_params.verbose)

    elif language in ('html','php'):
        return chunk_html_by_tag_blocks(text, task_params.max_tokens, task_params.model_name, task_params.encoding_name, verbose=task_params.verbose)


    else:
        return strict_token_chunking(text, task_params.max_tokens, task_params.model_name, task_params.encoding_name, task_params.overlap, task_params.verbose)
def chunk_html_by_tag_blocks(
    html: str,
    max_tokens: int = 1000,
    model_name: str = "gpt-4",
    encoding_name: str = None,
    tags: List[str] = None,
    verbose: bool = False
) -> List[str]:
    """
    Chunks HTML using BeautifulSoup, grouping by selected tag blocks (e.g., div, section).
    Each chunk is ≤ max_tokens.

    Args:
        html (str): HTML input.
        max_tokens (int): Max tokens per chunk.
        model_name (str): Token model name.
        encoding_name (str): Optional encoding override.
        tags (List[str]): Tags to treat as top-level chunks.
        verbose (bool): Print debug info.

    Returns:
        List[str]: List of HTML chunks.
    """
    task_params = get_class_inputs(ChunkParams,
                             max_tokens=max_tokens,
                             model_name=model_name,
                             encoding_name=encoding_name,
                             verbose=verbose,
                             tags=tags
                             
                            )
    tags = tags or ["section", "article", "div", "form", "main"]
    soup = BeautifulSoup(html, "html.parser")

    encoding = (
        tiktoken.get_encoding(task_params.encoding_name)
        if encoding_name else tiktoken.encoding_for_model(task_params.model_name)
    )

    def count_tokens(text):
        return len(encoding.encode(text))

    chunks = []
    current_chunk = ""
    current_tokens = 0

    for element in soup.find_all(tags, recursive=True):
        element_html = str(element)
        element_tokens = count_tokens(element_html)

        if element_tokens > task_params.max_tokens:
            # Include the element directly if it’s too large
            chunks.append(element_html)
            continue

        if current_tokens + element_tokens <= task_params.max_tokens:
            current_chunk += "\n" + element_html
            current_tokens += element_tokens
        else:
            chunks.append(current_chunk)
            current_chunk = element_html
            current_tokens = element_tokens

    if current_chunk:
        chunks.append(current_chunk)

    if task_params.verbose:
        print(f"Chunked into {len(chunks)} HTML segments")

    return chunks
def chunk_text_by_tokens(prompt_data,
                         max_tokens,
                         model_name="gpt-4",
                         encoding_name=None,
                         reverse=False):
    task_params = get_class_inputs(ChunkParams,
                             max_tokens=max_tokens,
                             model_name=model_name,
                             encoding_name=encoding_name,
                             reverse=reverse
                             
                            )
    sentences = prompt_data.split("\n")
    if task_params.reverse:
        sentences = reversed(sentences)

    chunks = []
    current_chunk = ""
    current_chunk_tokens = 0

    for sentence in sentences:
        sentence_tokens = num_tokens_from_string(sentence,task_params.smodel_name, task_params.encoding_name)

        if current_chunk_tokens + sentence_tokens <= task_params.max_tokens:
            current_chunk += "\n" + sentence if current_chunk else sentence
            current_chunk_tokens += sentence_tokens
        else:
            chunks.append(current_chunk)
            current_chunk = sentence
            current_chunk_tokens = sentence_tokens

    if current_chunk:
        chunks.append(current_chunk)

    return chunks
def chunk_by_braces(text,
                    max_tokens,
                    model_name,
                    encoding_name,
                    open='{',
                    close='}'):
    """
    Chunks code using balanced brace logic (useful for JS, PHP, etc.).
    """
    task_params = get_class_inputs(ChunkParams,
                             max_tokens=max_tokens,
                             model_name=model_name,
                             encoding_name=encoding_name
                            )
    encoding = (
        tiktoken.get_encoding(task_params.encoding_name)
        if encoding_name else tiktoken.encoding_for_model(task_params.model_name)
    )

    tokens = encoding.encode(text)
    decoded = encoding.decode(tokens)

    stack = []
    chunks = []
    buffer = ''
    for char in decoded:
        buffer += char
        if char == open:
            stack.append(char)
        elif char == close and stack:
            stack.pop()

        if not stack and len(encoding.encode(buffer)) >= task_params.max_tokens:
            chunks.append(buffer)
            buffer = ''

    if buffer.strip():
        chunks.append(buffer)

    return chunks

def extract_python_blocks(source_code: str, reverse: bool = False) -> List[str]:
    """
    Extracts top-level function and class definitions (including decorators) from Python source.

    Args:
        source_code (str): Python code to analyze.
        reverse (bool): Whether to extract blocks in reverse order.

    Returns:
        List[str]: List of code blocks (functions or classes).
    """
    reverse = reverse or False
    func_pattern = re.compile(r'^\s*def\s+\w+\s*\(.*\)\s*:', re.MULTILINE)
    class_pattern = re.compile(r'^\s*class\s+\w+\s*(\(.*\))?\s*:', re.MULTILINE)
    decorator_pattern = re.compile(r'^\s*@\w+', re.MULTILINE)

    lines = source_code.splitlines()
    if reverse:
        lines = list(reversed(lines))

    blocks = []
    current_block = []

    for line in lines:
        if func_pattern.match(line) or class_pattern.match(line):
            if current_block:
                if reverse:
                    blocks.append("\n".join(reversed(current_block)))
                else:
                    blocks.append("\n".join(current_block))
                current_block = []
        current_block.append(line)
        # Include decorators directly above function/class
        if decorator_pattern.match(line) and current_block:
            continue

    if current_block:
        if reverse:
            blocks.append("\n".join(reversed(current_block)))
        else:
            blocks.append("\n".join(current_block))

    return list(reversed(blocks)) if reverse else blocks
def chunk_source_code(source_code: str,
                      max_tokens: int,
                      model_name="gpt-4",
                      encoding_name=None,
                      reverse=False):
    task_params = get_class_inputs(ChunkParams,
                             max_tokens=max_tokens,
                             model_name=model_name,
                             encoding_name=encoding_name,
                             reverse=reverse
                            )
    encoding = (
        tiktoken.get_encoding(task_params.encoding_name)
        if task_params.encoding_name else tiktoken.encoding_for_model(task_params.model_name)
    )

    def token_count(text): return len(encoding.encode(text))

    chunks = []
    current_chunk = []
    current_tokens = 0

    blocks = extract_python_blocks(source_code, task_params.reverse)

    for block in blocks:
        block_tokens = token_count(block)
        if block_tokens > max_tokens:
            chunks.append(block)  # too big, include as is
        elif current_tokens + block_tokens <= task_params.max_tokens:
            current_chunk.append(block)
            current_tokens += block_tokens
        else:
            chunks.append("\n\n".join(current_chunk))
            current_chunk = [block]
            current_tokens = block_tokens

    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    return chunks


def strict_token_chunking(data: str,
                          max_tokens: int,
                          model_name: str = "gpt-4",
                          encoding_name: str = None,
                          overlap:int=0,
                          verbose:bool=False) -> List[str]:
    """
    Improved chunking method for descriptive summarization. This version uses paragraph-based boundaries
    and ensures token limits are respected. It preserves semantic coherence better than line-based splits.

    Args:
        data (str): The full input text.
        max_tokens (int): Maximum number of tokens per chunk.
        model_name (str): Model name for tokenization.
        encoding_name (str): Optional encoding override.

    Returns:
        List[str]: List of token-bound text chunks.
    """
    # Importing token counting utility
    task_params = get_class_inputs(ChunkParams,
                             max_tokens=max_tokens,
                             model_name=model_name,
                             encoding_name=encoding_name,
                             overlap=overlap,
                             verbose=verbose
                            )
    encoding = (
        tiktoken.get_encoding(task_params.encoding_name)
        if task_params.encoding_name
        else tiktoken.encoding_for_model(task_params.model_name)
    )

    def count_tokens(text):
        return len(encoding.encode(text))

    paragraphs = re.split(r"\n\s*\n", data.strip())  # split on paragraph gaps
    chunks = []
    current_chunk = []

    for paragraph in paragraphs:
        trial_chunk = "\n\n".join(current_chunk + [paragraph])
        if count_tokens(trial_chunk) <= task_params.max_tokens:
            current_chunk.append(paragraph)
        else:
            if current_chunk:
                chunks.append("\n\n".join(current_chunk))
            current_chunk = [paragraph]

    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    return chunks
