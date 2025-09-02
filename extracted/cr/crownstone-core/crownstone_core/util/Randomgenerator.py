"""
As we need consistent cross-platform pseudo random number generation. This is a port of the
Middle Square Weyl Sequence Random Number Generator found on https://mswsrng.wixsite.com/rand .
"""
from crownstone_core.util.Bitmasks import Bitmasks

class Msws:
    class State:
        def __init__(self, x , w, s):
            """
            x,w,s: int

            Note: s must be uneven for a proper Msws sequence
            """
            self.x = int(x) & Bitmasks.ff64
            self.w = int(w) & Bitmasks.ff64
            self.s = int(s) & Bitmasks.ff64

    def __init__(self, seed = None):
        """
        seed: int
        """
        if seed == None:
            # default seed
            self.state = Msws.State(0, 0, 0xb5ad4eceda1ce2a9)
        else:
            self.state = Msws._seed(seed)

    def get(self):
        """ Returns a random value and updates the self.state object. """
        return Msws._msws(self.state)

    @staticmethod
    def _msws(state):
        """
        Returns random value and updates the state objects internals values.

        state: State
        returns: int
        """
        state.x = (state.x * state.x) & Bitmasks.ff64
        state.w = (state.w + state.s) & Bitmasks.ff64
        state.x = (state.x + state.w) & Bitmasks.ff64
        state.x = ((state.x >> 32) | (state.x << 32)) & Bitmasks.ff64
        return state.x & Bitmasks.ff32

    seed_constants = [
        0x37e1c9b5e1a2b843, 0x56e9d7a3d6234c87, 0xc361be549a24e8c7, 0xd25b9768a1582d7b,
        0x18b2547d3de29b67, 0xc1752836875c29ad, 0x4e85ba61e814cd25, 0x17489dc6729386c1,
        0x7c1563ad89c2a65d, 0xcdb798e4ed82c675, 0xd98b72e4b4e682c1, 0xdacb7524e4b3927d,
        0x53a8e9d7d1b5c827, 0xe28459db142e98a7, 0x72c1b3461e4569db, 0x1864e2d745e3b169,
        0x6a2c143bdec97213, 0xb5e1d923d741a985, 0xb4875e967bc63d19, 0x92b64d5a82db4697,
        0x7cae812d896eb1a5, 0xb53827d41769542d, 0x6d89b42c68a31db5, 0x75e26d434e2986d5,
        0x7c82643d293cb865, 0x64c3bd82e8637a95, 0x2895c34d9dc83e61, 0xa7d58c34dea35721,
        0x3dbc5e687c8e61d5, 0xb468a235e6d2b193,
    ]

    @staticmethod
    def _seed(seed):
        """
        Returns an initial State object based on the given seed.

        seed: int
        returns: State
        """
        n = int(seed) & Bitmasks.ff64
        r = int(n / 100000000)
        t = int(n % 100000000)

        q = len(Msws.seed_constants)
        si = Msws.seed_constants[r % q] # must be uneven (true for given values in seed_constants)
        r//= q
        wi = t * si + r * si * 100000000
        xi = wi

        mswsi = Msws()
        mswsi.state = Msws.State(xi, wi, si)

        # get odd random number for low order digit
        u = (mswsi.get() % 8) * 2 + 1
        v = 1 << u

        # get rest of digits
        m = 60
        c = 0
        while m > 0:
            j = mswsi.get() # get 8 digit 32-bit random word

            for i in range(0,32,4):
                k = (j >> i) & 0xf # get a digit

                if k != 0 and (c & (1 << k)) == 0: # not 0 and not previous
                    c |= (1 << k)
                    u |= (k << m) # add digit to output
                    m -= 4
                    if m == 24 or m == 28:
                        c = (1 << k) | v
                    if m == 0:
                        break

        return Msws.State(u,u,u)

class RandomGenerator:
    def __init__(self, seed = None):
        """
        seed: int
        """
        self.engine = Msws(seed)

    def rand(self):
        """
        Return the next pseudo random number and update internal state.
        """
        return self.engine.get()

    def __call__(self):
        """
        Shorthand for self.rand()
        """
        return self.rand()

