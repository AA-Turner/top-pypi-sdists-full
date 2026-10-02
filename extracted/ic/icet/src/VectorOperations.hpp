#pragma once
#include <vector>

#include <Eigen/Dense>

#include "Hash.hpp"

using Eigen::Vector3i;

/// Hash function for a vector of ints.
struct VectorHash {
    /// Hash operator.
    size_t operator()(const std::vector<int>& v) const
    {
        size_t seed = 0;
        for (const int &i : v) {
            icet::hashCombine(seed, i);
        }
        return seed;
    }
};

/// Hash function for a three-dimensional vector.
struct Vector3iHash {
    /// Hash operator.
    size_t operator()(const Vector3i& v) const
    {
        size_t seed = 0;
        for (size_t i = 0; i < 3; i++) {
            icet::hashCombine(seed, v[i]);
        }
        return seed;
    }
};

/// Comparison operation for two three-dimensional vectors.
struct Vector3iCompare
{
    /// Comparison operator.
    bool operator()(const Vector3i &lhs, const Vector3i &rhs) const
    {
        for (size_t i = 0; i < 3; i++)
        {
            if (lhs[i] != rhs[i])
            {
                return lhs[i] < rhs[i];
            }
        }
        return false;
    }
};
