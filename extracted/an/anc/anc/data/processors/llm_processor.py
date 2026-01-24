from anc.data.anc_processor import Processor
from anc.data.anc_composer import SeqSplitConfig
from anc.data.processors.tokenizer import HFPretrainedTokenizer
import logging
import os
import sys
import torch
import json
from typing import List, Tuple


class FakeOpt:
    def __init__(self, hf_model_name, prompt_style, add_bos):
        self.hf_model_name = hf_model_name
        self.prompt_style = prompt_style
        self.prefix_template = ""
        self.delimiter = ""
        self.assistant_delimiter = None
        self.overall_prefix = None
        self.add_bos = add_bos
        self.do_capitalize = False


def setup_separate_prompt(opt):
    if opt.prompt_style == 'sunhao_old':
        opt.prefix_template = '### {role}:'
        opt.delimiter = '\n\n'
    # elif opt.prompt_style == 'chatml':
    #     opt.prefix_template = '<|im_start|> {role}\n'
    #     opt.delimiter = '<|im_end|>\n'
    elif opt.prompt_style == 'chatml2':
        opt.prefix_template = '<|im_start|>{role}\n'
        opt.delimiter = '<|im_end|>\n'
    elif opt.prompt_style == 'chatml_non_special': # used when <|im_end|> is not a special token
        opt.prefix_template = '<|im_start|> {role}\n'
        opt.delimiter = ' <|im_end|>\n'
    elif opt.prompt_style == 'llama3':
        opt.prefix_template = '<|start_header_id|>{role}<|end_header_id|>\n\n'
        opt.delimiter = '<|eot_id|>'
    elif opt.prompt_style == 'ds_v2':
        opt.prefix_template = '{role}: '
        opt.assistant_delimiter = '<｜end▁of▁sentence｜>'
        opt.delimiter = '\n\n'
        opt.do_capitalize = True
    elif opt.prompt_style == 'qwen':
        opt.prefix_template = '<|im_start|>{role}\n'
        opt.delimiter = '<|im_end|>\n'
    else:
        # Use chatml2 by default
        opt.prefix_template = '<|im_start|>{role}\n'
        opt.delimiter = '<|im_end|>\n'

    opt.delimiter = opt.delimiter.replace('\\n', '\n')
    logging.info(f'Using dialog template:\n{opt.prefix_template}content{opt.delimiter}')


class PretrainProcessor(Processor):
    """Processor class for pre-training language models.
    
    This class handles tokenization, sequence preparation, and batch creation for
    language model pre-training tasks.
    
    Attributes:
        tokenizer: HuggingFace tokenizer instance
        max_seq_len: Maximum allowed sequence length
        batch_size: Number of sequences per batch
        micro_batch_size: Number of sequences per micro-batch
        pad_token_id: Token ID used for padding
        special_tokens: List of special tokens to be added to tokenizer
        special_token_ids: List of token IDs corresponding to special tokens,
            since we may update the tokenizer config file directly to use reserved
            tokens as special tokens, we need to tell processor here to properly 
            handle them
        pad_to_max_seq_len: Whether to pad sequences to max_seq_len
        seq_split_config: Configuration for sequence splitting
    """
    def __init__(
        self,
        hf_model_name,
        max_seq_len,
        add_bos,
        batch_size,
        micro_batch_size,
        ceil_to_nearest=False,
        pad_label_id=None,
        cu_seqlen_use_old_pack=False,
        special_tokens=None,
        special_token_ids=None,
        pad_to_max_seq_len=False,
        seq_split_config=None,
        remove_special_tokens=True,
    ):
        self.opt = FakeOpt(hf_model_name, "", add_bos)
        self.tokenizer = HFPretrainedTokenizer(self.opt)
        self.max_seq_len = max_seq_len
        self.batch_size = batch_size
        self.micro_batch_size = micro_batch_size
        assert self.micro_batch_size == 1
        self.micro_batch = []
        self.pad_seq_length_to_mult = 16
        self.ceil_to_nearest = ceil_to_nearest
        self.pad_label_id = pad_label_id if pad_label_id is not None else self.tokenizer.end_token_id
        self.pad_token_id = self.tokenizer.end_token_id
        self.cu_seqlen_use_old_pack = cu_seqlen_use_old_pack
        self.pad_to_max_seq_len = pad_to_max_seq_len
        self.remove_special_tokens = remove_special_tokens
        if special_token_ids is None:
            special_token_ids = []
        if special_tokens is not None:
            if isinstance(special_tokens, str):
                special_tokens = [special_tokens]
            self.special_tokens = special_tokens
            self.tokenizer.add_special_tokens(special_tokens)
            special_token_ids += [self.tokenizer.txt2vec(i)[0] for i in self.special_tokens]
        else:
            self.special_tokens = []
        visited = set()
        remove_redundant_special_token_ids = []
        for i in special_token_ids:
            i = int(i)
            if i in visited:
                continue
            visited.add(i)
            remove_redundant_special_token_ids.append(i)
        self.special_token_ids = remove_redundant_special_token_ids
        added_tokens_decoder = self.tokenizer.added_tokens_decoder()
        for i in self.special_token_ids:
            assert i in added_tokens_decoder, f"{i} not in {added_tokens_decoder}"
        added_tokens = [added_tokens_decoder[i].content for i in self.special_token_ids]
        logging.warn(f"Added tokens are {added_tokens} with corresponding ids {self.special_token_ids}")
        if seq_split_config is None:
            seq_split_config = SeqSplitConfig()
        self.seq_split_config = seq_split_config
        self.all_masked_sample_cnt = 0
        self.sample_cnt = 0
        data_to_skip_path = os.getenv("ANC_DATA_TO_SKIP_PATH", None)
        # data_to_skip_path is a file that contains the data to skip, each line contains two columns: filepath and row_idx
        if data_to_skip_path is not None and os.path.exists(data_to_skip_path):
            data_to_skip = [line.strip().split() for line in open(data_to_skip_path, 'r')]
            self.data_to_skip = {(row[0], int(row[1])) for row in data_to_skip}
            logging.info(f"will skip {len(self.data_to_skip)} samples listed in {data_to_skip_path}")
        else:
            self.data_to_skip = set()

        try:
            self.too_long_sample_threshold = int(os.getenv("ANC_TOO_LONG_THRESHOLD"))
        except:
            self.too_long_sample_threshold = None

    def transform(self, item, is_last_sample=False):
        """Transform a text item into tokenized sequences with loss masks.
        
        Args:
            item: Dictionary containing 'content' key with text to process
            is_last_sample: Boolean indicating if this is the last sample
            
        Yields:
            Dictionary containing tokenized sequence and loss mask
        """
        if 'filepath' in item and 'row_idx' in item and (item['filepath'], item['row_idx']) in self.data_to_skip:
            logging.warning(f"skipping sample {item['filepath']}:{item['row_idx']} because it is in the skip list")
            return None
        tokens = self.tokenizer.txt2vec(item['content'])
        if self.too_long_sample_threshold is not None and len(tokens) > self.too_long_sample_threshold:
            logging.warning(f"Too long sample threshold is set, and sample length {len(tokens)} longer than threshold {self.too_long_sample_threshold}. Will drop")
            return None
        if len(tokens) > self.max_seq_len and not self.seq_split_config.allow_split:
            logging.warning(f"pretrain sample encounter with token length {len(tokens)} larger than {self.max_seq_len}, will ignore and continue")
            return None
        loss_mask = [1] * len(tokens)
        # set mask between two special tokens <MASK:Z0k7RxyNaZ> and </MASK:Z0k7RxyNaZ> to zero
        # may need more complex logic when we have more special tokens, or mask logic becomes more complex
        set_to_zero = False
        successive_zero_count = 0
        special_token_idxs = []
        for i in range(len(tokens)):
            if tokens[i] in self.special_token_ids:
                special_token_idxs.append(i)
                set_to_zero = not set_to_zero
                loss_mask[i] = 0
                successive_zero_count += 1
                if successive_zero_count >= self.max_seq_len:
                    # The context is too long, ignore this sample
                    logging.warn(f"The context (tokens between masks) is too long: {successive_zero_count}, will ignore current sample")
                    return None
            elif set_to_zero:
                loss_mask[i] = 0
                successive_zero_count += 1
                if successive_zero_count >= self.max_seq_len:
                    # The context is too long, ignore this sample
                    logging.warn(f"The context (tokens between masks) is too long: {successive_zero_count}, will ignore current sample")
                    return None
            else:
                successive_zero_count = 0
        # check if the first special token is the mask end token
        if special_token_idxs and self.tokenizer.vec2txt(tokens[special_token_idxs[0]]).startswith("</"):
            # flip the loss mask
            logging.warn(f"Flipping loss mask for sample from {item.get('filepath', 'unknown')}:{item.get('row_idx', 'unknown')}")
            special_token_idxs = set(special_token_idxs)
            for i in range(len(loss_mask)):
                if i not in special_token_idxs:
                    loss_mask[i] = 1 - loss_mask[i]

        # to remove special tokens from the input_ids
        if self.remove_special_tokens and special_token_idxs:
            special_token_idxs = set(special_token_idxs)
            new_tokens = [tokens[i] for i in range(len(tokens)) if i not in special_token_idxs]
            new_loss_mask = [loss_mask[i] for i in range(len(loss_mask)) if i not in special_token_idxs]
            tokens = new_tokens
            loss_mask = new_loss_mask
            assert len(tokens) == len(loss_mask)

        if sum(loss_mask) == 0:
            self.all_masked_sample_cnt += 1
            if self.sample_cnt >= 1000:
                logging.warn(f"Within last {self.sample_cnt} samples, {self.all_masked_sample_cnt} samples are all masked out.")
                self.all_masked_sample_cnt = 0
                self.sample_cnt = 0
            logging.debug(f"All tokens mask out for text {item['content']}, will ignore and continue")
            return None
        self.try_add_bos_token(tokens, loss_mask)
        self.sample_cnt += 1
        yield from [{"input_ids": tokens, "loss_mask": loss_mask, "text": item['content'], "row_idx": item['row_idx'], "filepath": item['filepath']}]

    # guide the composer to get the correct sequence length of each item
    def get_token_length_fn(self, item):
        """Get the length of a tokenized sequence. 
        Should be override by subclasses if dataset meta changes.
        
        Args:
            item: Dictionary containing 'input_ids' key
        Returns:
            int: Length of the token sequence
        """
        return len(item['input_ids'])

    # guide the composer to split a long sequence
    def split_fn(self, item, split_length):
        """Split a long sequence into two parts at the specified length.
        Should be override by subclasses if dataset meta changes.
        
        Args:
            item: Dictionary containing sequence data
            split_length: Length at which to split the sequence
            
        Returns:
            tuple: (first_part, second_part) of the split sequence
        """
        assert len(item['input_ids']) > split_length
        to_return = {
            'input_ids': item['input_ids'][:split_length],
            'loss_mask': item['loss_mask'][:split_length],
            'text': item['text'],
            'row_idx': item['row_idx'],
            'filepath': item['filepath'],
        }
        to_remain = {
            'input_ids': item['input_ids'][split_length:],
            'loss_mask': item['loss_mask'][split_length:],
            'text': item['text'],
            'row_idx': item['row_idx'],
            'filepath': item['filepath'],
        }
        return to_return, to_remain

    def try_add_bos_token(self, tokens, loss_mask):
        """Add beginning-of-sequence token if needed.
        
        Args:
            tokens: List of token IDs
            loss_mask: List of mask values corresponding to tokens
        """
        if self.opt.add_bos and tokens[0] != self.tokenizer.start_token_id:
            if self.tokenizer.start_token_id is None:
                return
            assert type(self.tokenizer.start_token_id) is int
            tokens.insert(0, self.tokenizer.start_token_id)
            loss_mask.insert(0, 0)  # Don't compute loss for BOS token

    def _compose_one_sequence(self, items):
        """Compose multiple items into a single sequence with necessary metadata.
        
        Args:
            items: Single item or list of items to compose
            
        Returns:
            dict: Dictionary containing:
                - tokens: Combined token IDs
                - labels: Shifted token IDs for language modeling
                - loss_mask: Mask indicating which tokens to compute loss for
                - position_ids: Position embeddings for each token
                - cu_seqlens: Cumulative sequence lengths
                - texts: Original text content if available
        """
        input_ids = []
        loss_mask = []
        labels = []
        position_ids = []
        cu_seqlens = []
        texts = []
        row_idxs = []
        filepaths = []
        valid_token_counts = []
        cur_seqlen = 0

        # Handle single item case
        if not isinstance(items, list):
            items = [items]

        # Combine all items into single sequences
        for item in items:
            input_ids += item['input_ids']
            # Shift labels by 1 for next-token prediction
            labels += item['input_ids'][1:] + [self.pad_label_id]
            loss_mask += item['loss_mask'][1:] + [0]
            cu_seqlens.append(cur_seqlen)
            cur_seqlen += len(item['input_ids'])
            position_ids += list(range(len(item['input_ids'])))
            if 'text' in item:
                texts.append(item['text'])
            if 'row_idx' in item:
                row_idxs.append(item['row_idx'])
            if 'filepath' in item:
                filepaths.append(item['filepath'])
            valid_token_counts.append(sum(item['loss_mask'][1:]))

        cu_seqlens.append(cur_seqlen)
        token_count = len(input_ids)

        # Pad sequence to max_seq_len if required
        if self.pad_to_max_seq_len:
            to_pad = self.max_seq_len - token_count
            if to_pad > 0:
                input_ids += [self.pad_token_id] * to_pad
                labels += [self.pad_label_id] * to_pad
                loss_mask += [0] * to_pad
                position_ids += [0] * to_pad
                token_count = self.max_seq_len

        # Convert lists to tensors
        res = {}
        res['tokens'] = torch.LongTensor(input_ids)
        res['labels'] = torch.LongTensor(labels)
        res['loss_mask'] = torch.LongTensor(loss_mask)
        res['position_ids'] = torch.LongTensor(position_ids)
        res['token_count'] = token_count
        res['cu_seqlens'] = cu_seqlens
        if texts:
            res['texts'] = texts
        if row_idxs:
            res['row_idxs'] = row_idxs
        if filepaths:
            res['filepaths'] = filepaths
        res['valid_token_counts'] = valid_token_counts
        return res

    def _collate_item(self, item, max_length, pad_id):
        """Pad a single item to the specified length.
        
        Args:
            item: Tensor to pad
            max_length: Target length after padding
            pad_id: Token ID to use for padding
            
        Returns:
            torch.Tensor: Padded tensor
        """
        item = torch.nn.functional.pad(
            item, 
            (0, max_length - item.shape[0]), 
            value=pad_id
        )
        return item

    def create_batch(self, items):
        """Create a batch from multiple sequences with proper padding.
        
        Handles padding and creation of attention masks and other metadata needed
        for transformer processing.
        
        Args:
            items: List of sequence dictionaries to batch
            
        Returns:
            dict: Batch dictionary containing:
                - tokens: Padded token sequences
                - labels: Padded label sequences
                - loss_mask: Padded loss masks
                - position_ids: Padded position embeddings
                - attention_mask: Batch attention mask
                - cu_seqlens: Cumulative sequence lengths
                - cu_seqlens_argmin: Indices of sequence starts
                - max_seqlen: Maximum sequence length in batch
        """
        res = {}
        # Find maximum token count in batch for padding
        max_token_count = max([i['token_count'] for i in items])
        if self.ceil_to_nearest:
            max_token_count = self._ceil_to_nearest(
                max_token_count, 
                self.pad_seq_length_to_mult
            )

        # Process each key in the items
        for k in items[0]:
            if k == 'tokens':
                res[k] = torch.stack([
                    self._collate_item(item[k], max_token_count, self.pad_token_id) 
                    for item in items
                ])
            elif k == 'labels':
                res[k] = torch.stack([
                    self._collate_item(item[k], max_token_count, self.pad_label_id) 
                    for item in items
                ])
            elif k in {'loss_mask', 'position_ids'}:
                res[k] = torch.stack([
                    self._collate_item(item[k], max_token_count, 0) 
                    for item in items
                ])
            elif k == 'token_count':
                res[k] = [item['token_count'] for item in items]
            elif k == 'cu_seqlens':
                # Handle cumulative sequence lengths
                for item in items:
                    if item[k][-1] < max_token_count:
                        if self.cu_seqlen_use_old_pack:
                            item[k][-1] = max_token_count
                        else:
                            item[k].append(max_token_count)
                    item[k] = torch.IntTensor(item[k])
                max_seq_count = max(len(item[k]) for item in items)
                res[k] = torch.stack([
                    self._collate_item(item[k], max_seq_count + 1, -1) 
                    for item in items
                ])
            elif k == 'texts':
                res[k] = [item[k] for item in items]
            elif k == 'row_idxs':
                res[k] = [item[k] for item in items]
            elif k == 'filepaths':
                res[k] = [item[k] for item in items]
            elif k == 'valid_token_counts':
                res[k] = [item[k] for item in items]

        # Create attention mask and other metadata
        res['attention_mask'] = torch.LongTensor([1] * len(items))
        res['cu_seqlens_argmin'] = torch.argmin(res['cu_seqlens'], dim=1, keepdim=True)
        seqlens = res['cu_seqlens'][:, 1:] - res['cu_seqlens'][:, :-1]
        max_seqlen, _ = seqlens.max(dim=1, keepdim=True)
        res['max_seqlen'] = max_seqlen
        # create cu_seqlens_unpadded, since we didn't pad any token between sequences 
        # during the sequence composing, we simply clone the cu_seqlens and cu_seqlens_argmin here
        res['cu_seqlens_unpadded'] = res['cu_seqlens'].clone()
        res['cu_seqlens_unpadded_argmin'] = res['cu_seqlens_argmin'].clone()
        return res

    def _ceil_to_nearest(self, n, m):
        """Round up to nearest multiple.
        
        Args:
            n: Number to round up
            m: Multiple to round to
            
        Returns:
            int: n rounded up to nearest multiple of m
        """
        return (n + m - 1) // m * m

    def batch_transform(self, list_of_items, is_last_batch=False):
        """Transform a list of items into batches.
        
        Args:
            list_of_items: List of sequences to batch
            is_last_batch: Whether this is the final batch
            
        Yields:
            dict: Processed batch of sequences
        """
        for items in list_of_items:
            one_sequence = self._compose_one_sequence(items)
            self.micro_batch.append(one_sequence)
            if len(self.micro_batch) == self.batch_size:
                one_batch = self.create_batch(self.micro_batch)
                self.micro_batch = []
                yield one_batch
                
        # Handle any remaining items in the last batch
        if is_last_batch and self.micro_batch:
            one_batch = self.create_batch(self.micro_batch)
            self.micro_batch = []
            yield one_batch

    def __getstate__(self):
        """Get object state for pickling."""
        return self.__dict__
    
    def __setstate__(self, states):
        """Set object state during unpickling."""
        self.__dict__.update(states)


class SFTProcessor(PretrainProcessor):
    """Processor for Supervised Fine-Tuning (SFT) of language models.
    
    Handles processing of conversational data with different roles (user, assistant, etc.)
    for supervised fine-tuning tasks. Inherits from PretrainProcessor.
    """
    def __init__(
        self,
        hf_model_name,
        prompt_style,
        max_seq_len,
        add_bos,
        batch_size,
        micro_batch_size,
        ceil_to_nearest=False,
        pad_label_id=None,
        cu_seqlen_use_old_pack=False,
        pad_to_max_seq_len=True,
        special_tokens=None,
        special_token_ids=None,
    ):
        """Initialize SFT processor with model and processing configurations.
        
        Args:
            hf_model_name: Name of the HuggingFace model to use
            prompt_style: Style template for formatting prompts
            max_seq_len: Maximum sequence length
            add_bos: Whether to add beginning-of-sequence token
            batch_size: Number of sequences per batch
            micro_batch_size: Size of micro-batches
            ceil_to_nearest: Whether to round sequence lengths up
            pad_label_id: ID to use for padding labels
            cu_seqlen_use_old_pack: Whether to use old packing method
        """
        super().__init__(
            hf_model_name,
            max_seq_len,
            add_bos,
            batch_size,
            micro_batch_size,
            ceil_to_nearest,
            pad_label_id,
            cu_seqlen_use_old_pack,
            pad_to_max_seq_len=pad_to_max_seq_len,
            special_tokens=special_tokens,
            special_token_ids=special_token_ids,
        )
        self.opt = FakeOpt(hf_model_name, prompt_style, add_bos)
        setup_separate_prompt(self.opt)

    def transform(self, item, is_last_sample=False):
        """Transform conversation data into model input format.
        
        Args:
            item: Dictionary containing conversation messages
            is_last_sample: Whether this is the last sample
            
        Yields:
            dict: Processed item
        """
        # if this is a pretrain data, delegate to pretrain processor
        if 'text' in item:
            pretrain_data = {"content": item['text']}
            if 'id' in item:
                pretrain_data['id'] = item['id']
            if 'filepath' in item:
                pretrain_data['filepath'] = item['filepath']
            if 'row_idx' in item:
                pretrain_data['row_idx'] = item['row_idx']
            yield from super().transform(pretrain_data, is_last_sample)
            return

        # Validate that all messages have required fields with correct types
        if not all(turn['role'] and turn['content'] and 
                  type(turn['role']) is str and type(turn['content']) is str 
                  for turn in item['messages']):
            logging.warn(f"Found an illegal sample and will skip it...")
            return
            
        # Process conversation context
        context = [(turn['role'].strip(), turn['content'], turn.get('no_loss', False)) for turn in item['messages']]
        last_turn_mask_flag = item.get('last_turn_mask', False) or item.get('loss_on_last_turn', False)
        no_mask_flag = item.get('no_mask', False)
        
        context_vec, loss_mask = self._encode_one(context, last_turn_mask_flag, no_mask_flag)
        if len(context_vec) > self.max_seq_len and not self.seq_split_config.allow_split:
            logging.warn(f"encounter sample with token length {len(context_vec)} larger than {self.max_seq_len}, will ignore and continue")
            return None
        # append one more token at the end of each sequence since nemo would truncate one
        # context_vec.append(self.tokenizer.end_token_id)
        # loss_mask.append(0)
        yield from [{"input_ids": context_vec, "loss_mask": loss_mask, "filepath": item["filepath"], "row_idx": item["row_idx"]}]

    def _encode_one(self, context, last_turn_mask_flag, no_mask_flag):
        """Encode a single conversation into token IDs and loss masks.
        
        Args:
            context: List of (role, content) tuples representing the conversation
            last_turn_mask_flag: Whether to only compute loss on the last turn
            no_mask_flag: Whether to disable masking
            
        Returns:
            tuple: (token_ids, loss_mask)
        """
        context_vec, loss_mask = self._build_chitchat_prompt(
            context,
            self.opt.delimiter,
            loss_on_last_turn=last_turn_mask_flag,
            enable_query_mask=no_mask_flag,
        )
        self.try_add_bos_token(context_vec, loss_mask)
        return context_vec, loss_mask

    def _build_chitchat_prompt(
        self,
        context: List[Tuple[str, str]], 
        dialog_sep: str=None, 
        loss_on_last_turn=False, 
        enable_query_mask=False, 
        add_generation_suffix=False,
        **kwargs
    ):
        """Build a formatted conversation prompt with appropriate masking.
        
        Args:
            context: List of (role, content) tuples for the conversation
            dialog_sep: Separator between dialogue turns
            loss_on_last_turn: Whether to only compute loss on the last turn
            enable_query_mask: Whether to disable masking for queries
            add_generation_suffix: Whether to add assistant prefix for generation
            
        Returns:
            tuple: (token_ids, loss_mask) for the formatted conversation
        """
        assert not (loss_on_last_turn and enable_query_mask)
        if dialog_sep is None:
            dialog_sep: str = self.opt.delimiter

        def _encode_one(prefix: str, content: str, suffix: str, is_output: bool = False):
            """Helper function to encode a single turn of conversation.
            
            Args:
                prefix: Role prefix template
                content: Message content
                suffix: Separator suffix
                is_output: Whether this is an assistant's output
                
            Returns:
                tuple: (role_tokens, content_tokens, suffix_tokens)
            """
            if is_output or enable_query_mask:
                # For assistant outputs or when no_query_mask is True,
                # encode role prefix separately from content
                encoded_role, encoded_content, encoded_suffix = (
                    self.tokenizer.txt2vec(prefix), 
                    self.tokenizer.txt2vec(content + suffix),
                    []
                )
            else:
                # For other roles, encode everything together
                encoded_role, encoded_content, encoded_suffix = (
                    [],
                    self.tokenizer.txt2vec(prefix + content + suffix),
                    []
                )
            return encoded_role, encoded_content, encoded_suffix

        idxs_encoded = []  # List to store all token IDs
        idxs_mask = []    # List to store loss mask values
        prefix_template: str = self.opt.prefix_template
        do_capitalize = self.opt.do_capitalize

        # Process each turn in the conversation
        for i, (role, content, no_loss) in enumerate(context):
            suffix_sep = dialog_sep

            if role == 'assistant':
                if do_capitalize:
                    role = role.capitalize()
                if self.opt.assistant_delimiter is not None:
                    suffix_sep = self.opt.assistant_delimiter
                # Handle assistant's responses
                encoded_role, encoded_content, encoded_suffix = _encode_one(
                    prefix_template.format(role=role), 
                    content, 
                    suffix_sep, 
                    is_output=True
                )
                # Set mask based on loss_on_last_turn flag
                if loss_on_last_turn:
                    to_learn = i == len(context) - 1
                else:
                    to_learn = not no_loss
                content_mask = [int(to_learn)] * len(encoded_content)
            else:
                # Handle other roles (user, system, etc.)
                if role not in ('user', 'human', 'system', 'document', 'memory', 
                              'function', 'ipython', 'tool', 'tool_calls'):
                    logging.warn(f"Found unknown role={role}")
                if do_capitalize:
                    role = role.capitalize()
                encoded_role, encoded_content, encoded_suffix = _encode_one(
                    prefix_template.format(role=role), 
                    content, 
                    suffix_sep
                )
                content_mask = [int(enable_query_mask)] * len(encoded_content)

            # Combine encoded parts and their masks
            idxs_encoded.extend(encoded_role + encoded_content + encoded_suffix)
            idxs_mask.extend([0] * len(encoded_role) + content_mask + [0] * len(encoded_suffix))

        # Add generation prefix if needed
        # incase need to add some token other than bos token
        if self.opt.overall_prefix is not None:
            idxs_encoded = self.tokenizer.txt2vec(self.opt.overall_prefix) + idxs_encoded
            idxs_mask = [0] * (len(idxs_encoded) - len(idxs_mask)) + idxs_mask
        if add_generation_suffix:
            idxs_encoded.extend(self.tokenizer.txt2vec(prefix_template.format(role='assistant')))
            idxs_mask.extend([0] * (len(idxs_encoded) - len(idxs_mask)))

        assert len(idxs_encoded) == len(idxs_mask)
        return idxs_encoded, idxs_mask


class SFTProcessorWithDecode(SFTProcessor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def decode_fn(self, line):
        item = json.loads(line)
        transformed = super().transform(item)
        if transformed is None:
            return []
        res = []
        for item in transformed:
            res.append(item)
        return res

    def transform(self, item, is_last_sample=False):
        yield from [item,]


class PPOProcessor:
    """Processor for handling data in PPO (Proximal Policy Optimization) training.
    
    This processor handles text tokenization and formatting for PPO-based training,
    including sequence length management and batch preparation.
    
    Attributes:
        tokenizer: Tokenizer instance for converting text to token IDs
        add_eod: Whether to append end-of-document token
        max_sample_length: Maximum allowed length for input samples
        collate_fn: Function for combining samples into batches
    """
    def __init__(self, cfg, tokenizer, collate_fn):
        """Initialize PPO processor with configuration and tokenizer.
        
        Args:
            cfg: Configuration object containing model and PPO parameters
            tokenizer: Tokenizer instance for text processing
            collate_fn: Function to collate samples into batches
        """
        self.tokenizer = tokenizer
        self.add_eod = cfg.model.data.get("append_eod", False)
        
        # Calculate maximum sample length based on sequence length and PPO config
        seq_length = cfg.model.data.seq_length
        if "length_params" in cfg.model.ppo:
            # Reserve space for PPO-specific length requirements
            max_sample_length = seq_length - cfg.model.ppo.length_params.max_length
        else:
            # Default to using half the sequence length
            max_sample_length = seq_length // 2
        self.max_sample_length = max_sample_length
        self.collate_fn = collate_fn

    def transform(self, sample, is_last_sample=False):
        """Transform a text sample into model input format.
        
        Converts text to token IDs and applies necessary formatting and length checks.
        
        Args:
            sample: Dictionary containing text data
            is_last_sample: Whether this is the last sample in the dataset
            
        Returns:
            list: List containing processed sample dictionary with:
                - text: Tensor of token IDs
                - length: Length of the sequence
                - loss_multiplier: Flag for loss calculation
                Returns None if sample exceeds maximum length
        """
        text = sample["text"]
        # Convert text to token IDs
        text_ids = self.tokenizer.text_to_ids(text)
        
        # Append end-of-document token if needed
        if len(text_ids) > 0 and self.add_eod:
            text_ids.append(self.tokenizer.eos_id)
            
        # Skip samples that exceed maximum length
        if len(text_ids) > self.max_sample_length:
            return
            
        # Convert to tensor and prepare output format
        sample_tensor = torch.tensor(text_ids, dtype=torch.int64)
        output = {
            "text": sample_tensor,
            "length": sample_tensor.shape[0],
            "loss_multiplier": True,  # Flag for loss calculation
        }
        return [output]
    
    def batch_transform(self, items, is_last_batch=False):
        """Transform a list of items into a batch.
        
        Args:
            items: List of processed samples to batch
            is_last_batch: Whether this is the final batch
            
        Returns:
            list: List containing single batched item created by collate_fn
        """
        return [self.collate_fn(items)]


class DPOProcessor(SFTProcessor):
    """Processor for Direct Preference Optimization (DPO) training.
    
    Handles processing of paired responses with preference rankings for DPO training.
    Inherits from SFTProcessor and adds preference-specific processing capabilities.
    
    Attributes:
        ensure_common_tokens: Whether to mask out common tokens between responses
        default_chosen_reward: Default reward value for chosen responses
        default_rejected_reward: Default reward value for rejected responses
        pad_reward_id: Padding value for reward tensors
    """
    def __init__(
        self,
        hf_model_name,
        prompt_style,
        max_seq_len,
        add_bos,
        batch_size,
        micro_batch_size,
        ceil_to_nearest=False,
        ensure_common_tokens=False,
        default_chosen_reward=1.0,
        default_rejected_reward=0.0,
        pad_label_id=-100,
        pad_reward_id=-1000,
        cu_seqlen_use_old_pack=False,
    ):
        """Initialize DPO processor with model and training configurations."""
        super().__init__(
            hf_model_name,
            prompt_style,
            max_seq_len,
            add_bos,
            batch_size,
            micro_batch_size,
            ceil_to_nearest,
            pad_label_id,
            cu_seqlen_use_old_pack,
        )
        self.ensure_common_tokens = ensure_common_tokens
        self.default_chosen_reward = default_chosen_reward
        self.default_rejected_reward = default_rejected_reward
        self.pad_reward_id = pad_reward_id
    
    def decode_fn(self, line):
        """Decode a JSON line into training examples with paired responses.
        
        Args:
            line: JSON string containing conversation and response data
            
        Returns:
            list: List of dictionaries containing messages and paired responses with ranks
        """
        session = json.loads(line)
        edited, chosen, rejected = session.get('edited', None), session.get('chosen', None), session.get('rejected', None)
        responses = []
        output = []
        
        # Collect valid responses
        if edited and edited.get('content'):
            responses.append(edited['content'])
        if chosen and chosen.get('content'):
            responses.append(chosen['content'])
        if rejected and rejected.get('content'):
            responses.append(rejected['content'])
            
        # Skip if not enough responses for comparison
        if len(responses) < 2:
            return output
        # Skip if last message is from assistant
        if session['messages'][-1]['role'] == 'assistant':
            return output

        # Create pairs of responses for comparison
        for i_yw in range(len(responses) - 1):
            for i_yl in range(i_yw + 1, len(responses)):
                if responses[i_yw] != responses[i_yl]:
                    output.append({
                        'messages': session['messages'],
                        'responses': [responses[i_yw], responses[i_yl]],
                        'ranks': [0, 1],
                    })
        return output

    def mask_common_token(self, yw_text_vec, yw_loss_mask, yl_text_vec, yl_loss_mask):
        """Mask out common tokens at the start and end of responses.
        
        Args:
            yw_text_vec: Token IDs for first response
            yw_loss_mask: Loss mask for first response
            yl_text_vec: Token IDs for second response
            yl_loss_mask: Loss mask for second response
        """
        # Mask common tokens from the start
        for i in range(min(len(yw_text_vec), len(yl_text_vec))):
            if yw_loss_mask[i] == yl_loss_mask[i] == 0:
                continue
            if yw_text_vec[i] == yl_text_vec[i]:
                yw_loss_mask[i] = yl_loss_mask[i] = -1
            else:
                break

        # Mask common tokens from the end
        for i in range(1, min(len(yw_text_vec), len(yl_text_vec))):
            if yw_loss_mask[-i] == yl_loss_mask[-i] == 0:
                continue
            if yw_text_vec[-i] == yl_text_vec[-i]:
                yw_loss_mask[-i] = yl_loss_mask[-i] = -1
            else:
                break

    def get_token_length_fn(self, item):
        """Get the length of the tokenized sequence.
        
        Args:
            item: input item
            
        Returns:
            int: Total length of the tokenized sequence
        """
        return len(item['yw_input_ids']) + len(item['yl_input_ids'])

    def transform(self, item, is_last_sample=False):
        """Transform a preference pair into model inputs.
        
        Args:
            item: Dictionary containing messages and paired responses
            is_last_sample: Whether this is the last sample
            
        Yields:
            dict: Processed inputs for both responses with rewards
        """
        context = [(turn['role'], turn['content']) for turn in item['messages']]
        responses = item['responses']
        ranks = item['ranks']
        yw_idx, yl_idx = 0, 1  # winner (yw) and loser (yl) indices
        assert ranks[yw_idx] < ranks[yl_idx]
        
        # Process both responses
        yw, yl = responses[yw_idx], responses[yl_idx]
        yw_context_vec, yw_loss_mask = self._encode_one(context + [('assistant', yw)], True, False)
        yl_context_vec, yl_loss_mask = self._encode_one(context + [('assistant', yl)], True, False)
        
        # Optionally mask common tokens
        if self.ensure_common_tokens:
            self.mask_common_token(yw_context_vec, yw_loss_mask, yl_context_vec, yl_loss_mask)
            
        yield from [{
            "yw_input_ids": yw_context_vec,
            "yw_loss_mask": yw_loss_mask,
            "yl_input_ids": yl_context_vec,
            "yl_loss_mask": yl_loss_mask,
            "chosen_reward": item.get("chosen_reward", self.default_chosen_reward),
            "rejected_reward": item.get("rejected_reward", self.default_rejected_reward)
        }]

    def _compose_one_sequence(self, items):
        """Compose a list of items into a single sequence.
        
        Args:
            items: List of dictionaries containing processed inputs
            
        Returns:
            dict: Composed sequence with rewards
        """
        if not isinstance(items, list):
            items = [items]
        res = super()._compose_one_sequence(items)
        res['rewards'] = torch.FloatTensor([i['reward'] for i in items])
        # loss_mask = res.pop('loss_mask')
        loss_mask = res['loss_mask']
        # nemo aligner use label < -1 as the loss mask
        # so we create the masked label inadvance here
        res['labels'][loss_mask==0] = self.pad_label_id
        return res

    def create_batch(self, items):
        """Create a batch from a list of items.
        
        Args:
            items: List of dictionaries containing processed inputs
            
        Returns:
            dict: Batched inputs ready for DPO training
        """
        res = super().create_batch(items)
        max_num_sequences = max(len(item['rewards']) for item in items)
        res['rewards'] = torch.stack([self._collate_item(item['rewards'], max_length=max_num_sequences, pad_id=self.pad_reward_id) for item in items])
        # nemo dpo needs input_ids instead of tokens
        res['input_ids'] = res.pop('tokens')
        return res

    def batch_transform(self, list_of_items, is_last_batch=False):
        """Transform a list of items into batches for DPO training.
        
        Args:
            list_of_items: List of preference pairs to process
            is_last_batch: Whether this is the final batch
            
        Yields:
            dict: Batched inputs ready for DPO training
        """
        for items in list_of_items:
            # Recreate items with proper structure for both chosen and rejected responses
            recreated_items = []
            if not isinstance(items, list):
                items = [items]
            for item in items:
                # Add chosen response
                recreated_items.append({
                    'input_ids': item['yw_input_ids'],
                    'loss_mask': item['yw_loss_mask'],
                    'reward': item['chosen_reward'],
                })
                # Add rejected response
                recreated_items.append({
                    'input_ids': item['yl_input_ids'],
                    'loss_mask': item['yl_loss_mask'],
                    'reward': item['rejected_reward'],
                })
                
            # Create and accumulate batches
            one_sequence = self._compose_one_sequence(recreated_items)
            self.micro_batch.append(one_sequence)
            if len(self.micro_batch) == self.batch_size:
                one_batch = self.create_batch(self.micro_batch)
                self.micro_batch = []
                yield one_batch
                
        # Handle any remaining items in the last batch
        if is_last_batch and self.micro_batch:
            one_batch = self.create_batch(self.micro_batch)
            self.micro_batch = []
            yield one_batch
