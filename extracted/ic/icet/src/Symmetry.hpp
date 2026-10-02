#pragma once

#include <algorithm>
#include <stdexcept>
#include <vector>

namespace icet
{

/**
Finds the permutation vector that takes v_permutation to v_original, and
returns true if there is one.

This is the non-throwing counterpart of getPermutation, intended for the call
sites at which the two vectors are not expected to be permutations of each
other in the first place, so that failure is an ordinary outcome rather than
an error.
*/
template <typename T>
bool tryGetPermutation(const std::vector<T> &v_original,
                       const std::vector<T> &v_permutation,
                       std::vector<int> &indices)
{
    if (v_original.size() != v_permutation.size())
    {
        return false;
    }

    indices.resize(v_original.size());

    for (size_t i = 0; i < v_original.size(); i++)
    {
        auto find = std::find(v_permutation.begin(), v_permutation.end(), v_original[i]);
        if (find == v_permutation.end())
        {
            return false;
        }
        indices[i] = std::distance(v_permutation.begin(), find);
    }

    return true;
}

/// Find the permutation vector that takes v_permutation to v_original
template <typename T>
std::vector<int> getPermutation(const std::vector<T> &v_original, const std::vector<T> &v_permutation)
{
    if (v_original.size() != v_permutation.size())
    {
        throw std::runtime_error("Vectors are not of the same size (Symmetry/getPermutation)");
    }

    std::vector<int> indices;
    if (!tryGetPermutation(v_original, v_permutation, indices))
    {
        throw std::runtime_error("Permutation not possible since vectors do not contain the same elements (Symmetry/getPermutation)");
    }

    return indices;
}

/// Returns the permutation of v using the permutation in indices.
template <typename T>
std::vector<T> getPermutedVector(const std::vector<T> &v,
                                 const std::vector<int> &indices)
{
    if (v.size() != indices.size())
    {
        throw std::runtime_error("Sizes of vectors do not match (Symmetry/getPermutedVector)");
    }

    std::vector<T> v2(v.size());
    for (size_t i = 0; i < v.size(); i++)
    {
        v2[i] = v[indices[i]];
    }
    return v2;
}

/// Returns the permutation of v using the permutation in indices.
template <typename T>
std::vector<std::vector<T>> getAllPermutations(std::vector<T> v)
{
    std::vector<std::vector<T>> allPermutations;
    std::sort(v.begin(), v.end());

    do
    {
        allPermutations.push_back(v);

    } while (std::next_permutation(v.begin(), v.end()));

    return allPermutations;
}

/// Returns the next cartesian product.
bool nextCartesianProduct(const std::vector<std::vector<int>> &items, std::vector<int> &currentProduct);

} // namespace icet
