import os
import re
import tiktoken
encoding = tiktoken.get_encoding("cl100k_base")
encoding = tiktoken.encoding_for_model("gpt-4")
encoding.encode("tiktoken is great!")
from abstract_utilities import write_to_file
from abstract_utilities.math_utils import find_common_denominator
def infer_tab_size(file_path):
    if not os.path.isfile(file_path):
        write_to_file(file_path=file_path,contents='\t')
    with open(file_path, 'r') as file:
        for line in file:
            if '\t' in line:
                # Assuming the first tab character aligns with a known indentation level
                return len(line) - len(line.lstrip())  # The length of indentation
    return 4  # Default if no tab found
def get_blocks(data, delim='\n'):
    if isinstance(data, list):
        return data, None
    if isinstance(data,tuple):
        data,delim=data[0],data[-1]
    if isinstance(data, list):
        return data, delim
    return data.split(delim), delim
def get_indent_levels(text):
    tab_size,indent_list = infer_tab_size('config.txt'),[0]
    for line in text.split('\n'):
        indent = 0
        for char in line:
            if char in [' ','\t']:
                if char == ' ':
                    indent+=1
                else:
                    indent +=tab_size
            else:
                break
    if indent not in indent_list:
        indent_list.append(indent)
    return indent_list

def num_tokens_from_string(string: str, encoding_name: str="cl100k_base") -> int:
    """
    Returns the number of tokens in a text string.

    Args:
        string (str): The input text.
        encoding_name (str, optional): The encoding name to use. Defaults to "cl100k_base".

    Returns:
        int: The count of tokens.
    """
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(str(string)))
    return num_tokens
def get_code_blocks(data,indent_level=0):
    blocks = [[]]
    def get_blocks(data,delim):
        if delim == None:
            if isinstance(data,str):
                data = list(data)
            delim = ''
        else:
            data = data.split(delim)
        return data,delim
    lines,delim = get_blocks(data,'\n')
    for line in lines:
        beggining=''
        for char in line:
            if char in ['',' ','\n','\t']:
                beggining +=char
            else:
                break
        if len(beggining) == indent_level:
            blocks[-1]=(delim).join(blocks[-1])
            blocks.append([line])
        else:
            blocks[-1].append(line)
    blocks[-1]=(delim).join(blocks[-1])
    return blocks,delim

def chunk_any_to_tokens(data, max_tokens, delimiter='\n\n', reverse=False):
    """
    Splits the given data into chunks based on the provided chunking strategy.

    Args:
        blocks (list): The data blocks to be chunked.
        max_tokens (int): The maximum number of tokens each chunk can have.
        delimiter (str, optional): The delimiter to use when joining blocks. Defaults to ''.
        reverse (bool, optional): If True, reverse the order of the blocks. Defaults to False.

    Returns:
        list of str: A list of data chunks based on the specified chunking strategy.
    """
    if isinstance(data,list):
        blocks=data
    else:
        blocks,delimiter = get_blocks(data,delimiter)

    if reverse:
        blocks = reversed(blocks)

    chunks = []
    current_chunk = []

    for block in blocks:
        if num_tokens_from_string(delimiter.join(current_chunk + [block])) <= max_tokens:
            current_chunk.append(block)
        else:
            if current_chunk:
                chunks.append(delimiter.join(current_chunk))
            current_chunk = [block]  # Start a new chunk

    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(''.join(current_chunk))

    return chunks



def chunk_data_by_type(data, max_tokens,chunk_type=None,reverse=False):
    delimeter=None
    if chunk_type == "URL":
        delimeter=None
        blocks = re.split(r'<h[1-6].*?>.*?</h[1-6]>', data)
    if chunk_type == "SOUP":
        delimeter=None
        blocks = data
    elif chunk_type == "DOCUMENT":
        delimeter = "."
        blocks = data.split(delimeter)
    elif chunk_type == "CODE":
        chunks = chunk_source_code(data,max_tokens,reverse=reverse)
        for each in ['',' ','\n','\t']:
            while each in chunks:
                chunks.remove(each)
        return chunks
    elif chunk_type=="TEXT":
        chunks = chunk_text_by_tokens(data, max_tokens,reverse=reverse)
        for each in ['',' ','\n','\t']:
            while each in chunks:
                chunks.remove(each)
        return chunks
    else:
        delimeter="\n\n"
        blocks = data.split(delimeter)
    return chunk_any_to_tokens(blocks,max_tokens,delimeter,reverse=reverse)
def chunk_text_by_tokens(prompt_data, max_tokens, reverse=False):
    """
    Chunks text data by tokens, ensuring that no chunk exceeds the maximum token limit.
    If reverse is True, chunks from the end of the text instead of the beginning.

    Args:
        prompt_data (str): The text data to be chunked.
        max_tokens (int): The maximum number of tokens per chunk.
        reverse (bool): If True, chunking starts from the end of the text.

    Returns:
        list of str: A list of strings where each string represents a chunk of the original text.
    """
    # Reverse the sentences if chunking from the end
    sentences = prompt_data.split("\n")
    if reverse:
        sentences = reversed(sentences)

    chunks = []
    current_chunk = ""
    current_chunk_tokens = 0

    for sentence in sentences:
        sentence_tokens = num_tokens_from_string(sentence)

        # Check if adding the next sentence exceeds the max token count
        if current_chunk_tokens + sentence_tokens <= max_tokens:
            if reverse:
                current_chunk = sentence + "\n" + current_chunk
            else:
                current_chunk += "\n" + sentence
            current_chunk_tokens += sentence_tokens
        else:
            # If chunking from the end, prepend new chunks
            if reverse and current_chunk:
                chunks.insert(0, current_chunk)
            else:
                chunks.append(current_chunk)
            current_chunk = sentence
            current_chunk_tokens = sentence_tokens

    # Don't forget the last chunk
    if current_chunk:
        if reverse:
            chunks.insert(0, current_chunk)
        else:
            chunks.append(current_chunk)

    return chunks
def extract_functions_and_classes(source_code,reverse=False):
    """
    Extracts and separates all the functions and classes from the provided source code.

    Args:
        source_code (str): A string containing the source code from which functions and classes are to be extracted.

    Returns:
        list of str: A list where each element is a string containing a single function or class definition.
    """
    functions_and_classes = []
    # Regular expressions to match function and class definitions
    func_pattern = re.compile(r'^\s*def\s+\w+\s*\(.*\):')
    class_pattern = re.compile(r'^\s*class\s+\w+\s*\(.*\):')
    
    lines = source_code.splitlines()
    current_block = []
    if reverse:
        lines = reversed(lines)
    for line in lines:
        
        if func_pattern.match(line) or class_pattern.match(line):
            functions_and_classes.append("\n".join(current_block))
            current_block = []
        current_block.append(line)
    if current_block:
        functions_and_classes.append("\n".join(current_block))        
    return functions_and_classes
def chunk_source_code(source_code, max_tokens,reverse=False):
    """
    Chunks source code into segments that do not exceed a specific token limit, focusing on keeping functions and classes intact.

    Args:
        source_code (str): The source code to be chunked.
        max_tokens (int): The maximum number of tokens allowed in each chunk.

    Returns:
        list of str: A list of source code chunks, each within the specified token limit.
    """
    if reverse:
        functions_and_classes = reversed(functions_and_classes)
    # Initialize the function analyzer.
    chunks=['']
    functions_and_classes=extract_functions_and_classes(source_code)
    for block in functions_and_classes:
        if num_tokens_from_string(block) > max_tokens:
            chunks=chunks+chunk_data_by_type(block, max_tokens)
        elif num_tokens_from_string(chunks[-1] + block) > max_tokens:
            chunks.append(block)
        else:
            chunks[-1]+= '\n'+block
    return chunks
