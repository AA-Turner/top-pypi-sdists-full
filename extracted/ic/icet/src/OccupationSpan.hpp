#pragma once

#include <cstddef>

/**
@brief A non-owning, read-only view of a contiguous sequence of occupations.
@details
    Stands in for std::span<const int> (C++20) under this project's C++17
    baseline.
    Deliberately a plain, fully inline class rather than a template, so that
    indexing is as cheap to inline as indexing a raw pointer; see
    benchmark/README.md for how an inlining regression in a counting loop
    that reads through a class like this one is checked for and caught.
*/
class OccupationSpan
{
public:
    constexpr OccupationSpan(const int *data, size_t size) : _data(data), _size(size) {}

    constexpr const int &operator[](size_t index) const { return _data[index]; }
    constexpr size_t size() const { return _size; }
    constexpr const int *data() const { return _data; }

private:
    const int *_data;
    size_t _size;
};
