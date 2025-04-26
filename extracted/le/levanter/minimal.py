import jax
jax.config.update('jax_array', True)  # required for jax<0.4.0
import jax.numpy as jnp
from jax.sharding import Mesh
from jax.experimental.pjit import pjit, with_sharding_constraint
from jax.sharding import PartitionSpec as P
from functools import partial
import numpy as np

num_layers = 48
num_heads = 24
head_size = 64
embed_size = 1536

# batch = 512
# seq_len = 16384
# block_len = 2048
batch = 8
seq_len = 1024
block_len = 256

qkv_sharding = P(None, None, None, 'data')
x_sharding = P('data', None, 'model', None)
o_sharding = P(None, None, 'model', 'data')

qkv = jnp.ones((num_layers, num_heads, head_size, embed_size), dtype=jnp.bfloat16)
o = jnp.ones((num_layers, num_heads, head_size, embed_size), dtype=jnp.bfloat16)
x = jnp.ones((batch, seq_len, embed_size), dtype=jnp.bfloat16)

dp, mp = len(jax.local_devices()), 1
devices = np.reshape(jax.local_devices(), (dp, mp))
mesh = Mesh(devices, ('data', 'model'))
x = jax.device_put(x, jax.sharding.MeshPspecSharding(mesh, x_sharding))
qkv = jax.device_put(qkv, jax.sharding.MeshPspecSharding(mesh, qkv_sharding))
o = jax.device_put(o, jax.sharding.MeshPspecSharding(mesh, o_sharding))

params = (qkv, o)

def pseudo_sliding_window_attention(x):
    # (this is not attention, but is minimized from attn)
    # dims are [batch, len, num_heads, head_dim]
    # having num_heads is important. num_heads = 1, no boom
    def block(block_idx):
        query_block = jax.lax.dynamic_slice_in_dim(x, block_idx, block_len, axis=1)
        weights = jnp.sum(query_block, axis=3) # [batch, len, num_heads]
        weights = jax.lax.broadcast_in_dim(weights, (batch, block_len, num_heads, block_len), (0, 1, 2))  # [batch, len, num_heads, len]
        weights = with_sharding_constraint(weights, P('data', None, None, None))
        # without "bias", no boom
        bias = jnp.ones(block_len).broadcast_in_dim((batch, block_len, num_heads, block_len), (1,))
        weights = weights + bias
        return jnp.einsum('bqhk,bkhd->bqhd', weights, query_block).astype(query_block.dtype)

    num_blocks = seq_len // block_len
    blocked_attn = jax.lax.map(block, jnp.arange(0, num_blocks))  # [num_blocks, batch, len, num_heads, head_dim]
    blocked_attn = jnp.concatenate(blocked_attn, axis=1)

    return blocked_attn


def fwd(params, x):
    @partial(jax.checkpoint, prevent_cse=False)
    def layer(x, params):
        qkv, o = params
        y = jnp.einsum('bte,hde->bthd', x, qkv)
        y = pseudo_sliding_window_attention(y)
        z = jnp.einsum('bthd,hde->bte', y, o)
        return z, None

    x, _ = jax.lax.scan(layer, x, params)

    return x

def loss_fn(params, x):
    x = fwd(params, x)
    l = jnp.mean(x)
    return l

def grad_fn(params, x):
    loss, grad = jax.value_and_grad(loss_fn)(params, x)
    return loss, grad

with mesh:
    loss, grad = pjit(grad_fn)(params, x)
    loss.block_until_ready()
