#pragma once

#include <cstddef>
#include <cstdint>
#include <type_traits>

/**
@file
Hash combination utilities.

`hashCombine` folds the hash of a value into a running seed, so that a compound
key can be hashed by combining the hashes of the individual parts. It backs the
hash functions for lattice sites, for vectors of lattice sites, and for vectors
of integers.

Three mixing steps are provided. Which one applies depends on how wide `size_t`
is and on whether it names the same type as `uint32_t` or `uint64_t`, so hash
values differ between platforms. That is acceptable because the values only
determine how entries are distributed over the buckets of an unordered
container. Do not store a hash value, transfer one between platforms, or depend
on the iteration order of a container that is keyed by one.
**/

namespace icet
{

    namespace hashDetail
    {

        /**
        @brief Combines a hash value into a seed.
        @details
            This step applies when `size_t` names neither `uint32_t` nor
            `uint64_t`, which on common platforms means a `size_t` that is 64
            bits wide but is a distinct type from `uint64_t`.

            The constant is derived from the golden ratio and spreads the bits
            of the combined value across the seed.
        @param seed hash value to update
        @param value hash value to combine into the seed
        **/
        template <typename SizeT>
        inline void hashCombineImpl(SizeT &seed, SizeT value)
        {
            seed ^= value + 0x9e3779b9 + (seed << 6) + (seed >> 2);
        }

        /**
        @brief Combines a hash value into a seed using a 32-bit hash width.
        @details
            This is the mixing step of the 32-bit MurmurHash3 algorithm, which
            is in the public domain. It applies when `size_t` names the same
            type as `uint32_t`.
        @param seed hash value to update
        @param value hash value to combine into the seed
        **/
        inline void hashCombineImpl(uint32_t &seed, uint32_t value)
        {
            const uint32_t c1 = 0xcc9e2d51;
            const uint32_t c2 = 0x1b873593;

            value *= c1;
            value = (value << 15) | (value >> 17);
            value *= c2;

            seed ^= value;
            seed = (seed << 13) | (seed >> 19);
            seed = seed * 5 + 0xe6546b64;
        }

        /**
        @brief Combines a hash value into a seed using a 64-bit hash width.
        @details
            This is the mixing step of the 64-bit MurmurHash2 algorithm, which
            is in the public domain. It applies when `size_t` names the same
            type as `uint64_t`. That is the case on 64-bit Linux, and it is
            therefore the step that normally runs.
        @param seed hash value to update
        @param value hash value to combine into the seed
        **/
        inline void hashCombineImpl(uint64_t &seed, uint64_t value)
        {
            const uint64_t m = UINT64_C(0xc6a4a7935bd1e995);
            const int r = 47;

            value *= m;
            value ^= value >> r;
            value *= m;

            seed ^= value;
            seed *= m;

            // Arbitrary constant that keeps zeros from hashing to zero.
            seed += 0xe6546b64;
        }

    }

    /**
    @brief Combines the hash of an integer value into a seed.
    @details
        The hash of an integer is the value itself, converted to `size_t`, so
        all of the mixing is carried out by the combination step.

        Only integer types are accepted. That identity is not a suitable hash
        for a floating point value, where distinct representations such as
        `0.0` and `-0.0` compare equal and therefore have to hash equally.
    @param seed hash value to update
    @param value integer whose hash is combined into the seed

    **Example:**

        size_t seed = 0;
        icet::hashCombine(seed, index);
        for (size_t i = 0; i < 3; i++)
        {
            icet::hashCombine(seed, offset[i]);
        }
    **/
    template <typename T>
    inline void hashCombine(size_t &seed, T value)
    {
        static_assert(std::is_integral<T>::value,
                      "icet::hashCombine only accepts integer values");
        hashDetail::hashCombineImpl(seed, static_cast<size_t>(value));
    }

}
