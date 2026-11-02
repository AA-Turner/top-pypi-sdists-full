from sys import getrefcount
from _rl_accel import calcChecksum

print(f'{calcChecksum(b"Hello cruel world!")=}')
