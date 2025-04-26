import jax
from jax.sharding import PartitionSpec as P
from jax.experimental.pjit import pjit
from jaxlib.xla_client import NamedSharding


def f(data, key):
    return jax.random.normal(key, ()) + data

key = jax.random.PRNGKey(1)

devices = jax.local_devices()
mesh = Mesh(devices, ('dp',))

print(devices)

data = jax.random.normal(key, (len(devices),))
sharding = NamedSharding(mesh, P('dp',))
data = jax.device_put(data, sharding)

with mesh:
    # As you can see, using host_local_array_to_global_array is not required since in_axis_resources says
    # that the input is fully replicated via P(None)
    # The input is fully replicated across all devices
    # The output is fully replicated across all devices
    pjit(f, in_shardings=(sharding, None), out_shardings=sharding)(data, key)
