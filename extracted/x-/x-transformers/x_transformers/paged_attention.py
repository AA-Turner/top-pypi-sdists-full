from __future__ import annotations

import torch
from torch import nn, Tensor
from torch.nn import Module
import torch.nn.functional as F

from einops import rearrange

# helpers

def exists(val):
    return val is not None

def default(val, d):
    return val if exists(val) else d

def ceil_div(num, den):
    return -(-num // den)

# paged attention

def paged_attention(
    q: Tensor,
    k_pages: Tensor,
    v_pages: Tensor,
    block_table: Tensor,
    seq_len: int,
    causal = True
) -> Tensor:
    """q: (b n h d) | pages: (num_pages page_size h d) | block table: (b num_blocks)"""

    k, v = [
        rearrange(pages[block_table], 'b blocks page h d -> b h (blocks page) d')[:, :, :seq_len]
        for pages in (k_pages, v_pages)
    ]

    n = q.shape[1]
    q = rearrange(q, 'b n h d -> b h n d')

    mask = None
    if causal:
        mask = torch.ones((n, seq_len), dtype = torch.bool, device = q.device).tril(seq_len - n)

    out = F.scaled_dot_product_attention(q, k, v, attn_mask = mask)
    return rearrange(out, 'b h n d -> b n h d')

class PagedKVCache:
    def __init__(self, page_size = 16):
        self.page_size = page_size
        self.k = self.v = self.block_table = None
        self.seq_len = 0

    def append(self, k: Tensor, v: Tensor):
        """k, v: (b n h d), appends a uniform chunk of tokens for every batch"""

        b, n, h, d = k.shape
        page_size = self.page_size
        block_table = default(self.block_table, k.new_zeros((b, 0), dtype = torch.long))

        num_blocks = ceil_div(self.seq_len + n, page_size)
        num_new_blocks = num_blocks - block_table.shape[-1]

        if num_new_blocks > 0:
            k_pages = default(self.k, k.new_zeros((0, page_size, h, d)))
            v_pages = default(self.v, v.new_zeros((0, page_size, h, d)))
            new_pages = k_pages.shape[0] + rearrange(torch.arange(b * num_new_blocks, device = k.device), '(b blocks) -> b blocks', b = b)

            self.k = torch.cat((k_pages, k.new_zeros((b * num_new_blocks, page_size, h, d))))
            self.v = torch.cat((v_pages, v.new_zeros((b * num_new_blocks, page_size, h, d))))
            block_table = torch.cat((block_table, new_pages), dim = -1)

        self.block_table = block_table

        pos = self.seq_len + torch.arange(n, device = k.device)
        offsets = pos % page_size
        slots = block_table[:, pos // page_size]

        self.k[slots, offsets] = k
        self.v[slots, offsets] = v
        self.seq_len += n

class PagedAttention(Module):
    def __init__(
        self,
        dim,
        dim_head = 64,
        heads = 8,
        page_size = 16,
        causal = True
    ):
        super().__init__()
        self.heads = heads
        self.page_size = page_size
        self.causal = causal

        self.to_qkv = nn.Linear(dim, 3 * heads * dim_head, bias = False)
        self.to_out = nn.Linear(heads * dim_head, dim, bias = False)

    def forward(self, x, cache = None):
        q, k, v = rearrange(self.to_qkv(x), 'b n (qkv h d) -> qkv b n h d', qkv = 3, h = self.heads)

        cache = default(cache, PagedKVCache(page_size = self.page_size))
        cache.append(k, v)

        out = paged_attention(q, cache.k, cache.v, cache.block_table, cache.seq_len, self.causal)
        return self.to_out(rearrange(out, 'b n h d -> b n (h d)')), cache
