import json
import numpy as np
import random

def count_words_in_string(string):
    return len(string.split())

def count_tokens_in_string(string, tokenizer):
    tokens = tokenizer(string).input_ids
    return len(tokens)

def find_common_prefix_between_two_strings(str1, str2):
    # Early exit for empty strings
    if not str1 or not str2:
        return ""
    
    # Use zip for faster iteration
    return ''.join(x for x, y in zip(str1, str2) if x == y)

def find_common_prefix_between_two_list(list1, list2):
    # Early exit for empty strings
    common_prefix = []
    # Use zip for faster iteration
    for i in range(min(len(list1), len(list2))):
        if list1[i] == list2[i]:
            common_prefix.append(list1[i])
        else:
            break
    return common_prefix

def print_percentiles(data_list, name=""):
    """Print p0, p25, p50, p90, p99, p100 for a list of values"""
    percentiles = np.percentile(data_list, [0, 25, 50, 90, 99, 100])
    print(f"{name} percentiles:")
    print(f"  p0  (min): {percentiles[0]:.2f}")
    print(f"  p25      : {percentiles[1]:.2f}")
    print(f"  p50 (med): {percentiles[2]:.2f}")
    print(f"  p90      : {percentiles[3]:.2f}")
    print(f"  p99      : {percentiles[4]:.2f}")
    print(f"  p100 (max): {percentiles[5]:.2f}")

# Count total lines first
def get_line_count(file_path):
        with open(file_path, 'r') as f:
            return sum(1 for _ in f)
    
    

def process_input_data(file_path, tokenizer_path=None, sample_size=10):
    tokenizer = None
    if tokenizer_path:
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
        print(f"Using tokenizer: {tokenizer_path}")

    # Read the JSON file
    from tqdm import tqdm
    common_prefix_token_len_list = []
    common_prefix_word_len_list = []
    token_count_list = []
    word_count_list = []
    messages = []
    tokenizerd_messages = []
    total_lines = get_line_count(file_path)
    print(f"Processing {total_lines} lines...")
    with open(file_path, 'r') as f:
        for line in tqdm(f, total=total_lines):
            data = json.loads(line)
            message = data["messages"][0]["content"]
            if tokenizer:
                token_count_list.append(count_tokens_in_string(message, tokenizer))
                tokenized_message = tokenizer(message).input_ids
            
            # Compare with random sample of previous messages
            if messages:
                sample = random.sample(messages, min(sample_size, len(messages)))
                for prev_msg in sample:
                    prefix = find_common_prefix_between_two_strings(prev_msg, message)
                    common_prefix_word_len_list.append(count_words_in_string(prefix))
            if tokenizer:
                for prev_tokenized_message in tokenizerd_messages:
                    common_prefix = find_common_prefix_between_two_list(prev_tokenized_message, tokenized_message)
                    common_prefix_token_len_list.append(len(common_prefix))
            
            if tokenizer:
                tokenizerd_messages.append(tokenized_message)
            messages.append(message)
            word_count_list.append(count_words_in_string(message))

    if tokenizer:
        print("\n=== Token Statistics ===")
        print(f'Average token count: {sum(token_count_list) / len(token_count_list):.2f}')
        print_percentiles(token_count_list, "Token counts")
        
        print("\n=== Token Common Prefix Statistics ===")
        print(f'Average common prefix token count: {sum(common_prefix_token_len_list) / len(common_prefix_token_len_list):.2f}')
        print_percentiles(common_prefix_token_len_list, "Common prefix token counts")

    print("\n=== Word Statistics ===")
    print(f'Average word count: {sum(word_count_list) / len(word_count_list):.2f}')
    print_percentiles(word_count_list, "Word counts")

    print("\n=== Word Common Prefix Statistics ===")
    print(f'Average common prefix word count: {sum(common_prefix_word_len_list) / len(common_prefix_word_len_list):.2f}')
    print_percentiles(common_prefix_word_len_list, "Common prefix word counts")

if __name__ == "__main__":
    import argparse
    import os
    
    parser = argparse.ArgumentParser(description='Process and duplicate background information in conversation data.')
    parser.add_argument('input_file', type=str, help='Path to the input JSONL file')
    parser.add_argument('--tokenizer', type=str, required=False, help='Name of the tokenizer to use for token counting, if not proviced, will only count word not token')
    
    args = parser.parse_args()
    
    input_file = args.input_file
    tokenizer_path = args.tokenizer

    process_input_data(input_file, tokenizer_path)
