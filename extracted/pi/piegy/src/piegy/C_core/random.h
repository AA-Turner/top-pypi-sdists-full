/**
 * The Random Number Generation module
 * Returns a random double in (0, 1) with 2^-53 resolution, 0 and 1 not included
 * 
 * First initialize xoshiro256+ states with Splitmix64
 * Then use xoshiro256+ for random number generation
 * 
 * Referrence:
 * xoshiro256++ code: https://prng.di.unimi.it
 * Splitmix64 code: https://rosettacode.org/wiki/Pseudo-random_numbers/Splitmix64
 * 
*/

#include <stdint.h>


// resolution of random01 is 2^-53
// which is the IEEE 754 double precision
#define MAX_53BIT (uint64_t) ((1ULL << 53) - 1)
#define RAND_DENOM 1.0 / ((double) (1ULL << 53))
// xor_state
static uint64_t xor_state[4];
static uint64_t splitmix64_state;



static inline uint64_t Splitmix64_rand() {
    // used to seed PCG initial states
    splitmix64_state += 0x9e3779b97f4a7c15ULL;
    uint64_t z = splitmix64_state;
    z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
    z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL;
    return z ^ (z >> 31);
}


static inline uint64_t rot23(const uint64_t x) {
    // 23 and 64 - 23
    // Not used here, part of xoshiro256++
	return (x << 23) | (x >> 41);
}


static inline uint64_t rot45(const uint64_t x) {
    // 45 and 64 - 45
	return (x << 45) | (x >> 19);
}


static inline double random01() {
    // return a random number in (0, 1) with 2^-53 resolution. 0 and 1 not included.

	const uint64_t result = xor_state[0] + xor_state[3];
    const uint64_t t = xor_state[1] << 17;

	xor_state[2] ^= xor_state[0];
	xor_state[3] ^= xor_state[1];
	xor_state[1] ^= xor_state[2];
	xor_state[0] ^= xor_state[3];

    xor_state[2] ^= t;
	xor_state[3] = rot45(xor_state[3]);

	return ((double) (result & MAX_53BIT) + 0.5) * RAND_DENOM;
}


static inline void rand_init(const uint64_t seed) {
    // initialize xorshift RNG
    splitmix64_state = seed;
    for (int i = 0; i < 4; i++) {
        xor_state[i] = Splitmix64_rand();
    }
    (void) random01();
}


