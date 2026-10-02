#pragma once

#include <algorithm>
#include <cstddef>
#include <cstdint>
#include <vector>

/**
@brief Accumulates the weighted occupation patterns of counted clusters.
@details
    Counting a cluster produces one pattern, meaning the species that occupy
    its sites, together with a weight. The clusters of an orbit fall into far
    fewer distinct patterns than there are clusters, so counting coalesces:
    all clusters that carry the same pattern contribute to one entry.

    A pattern is an integer, encoded from the per-site species indices as
    described by OrbitEvaluationPlan. Distinct patterns therefore have
    distinct codes, and the codes of two patterns compare in the same order
    as the patterns themselves compare position by position.

    The entries live in an open-addressing table with linear probing and a
    capacity that is a power of two, so locating the entry of a pattern is a
    mask and, in the common case, one comparison.

    Ownership and allocation
    ------------------------

    A buffer belongs to one evaluation. An entry point creates one, prepares
    it once per orbit, and lets it go when it returns, so nothing is shared
    between two evaluations and the entry points stay const and reentrant.
    Because prepare() only ever grows the storage and empties the table by
    clearing the slots that were used rather than the whole table, the
    allocations happen on the first prepare of a call and the counting loops
    themselves allocate nothing at all.

    The table is kept at most half full, so probing always terminates on an
    empty slot. The number passed to prepare() is a hint rather than a
    promise: if more distinct patterns turn up than it allowed for, the
    table grows. That path allocates, but it is reached only when the hint
    was too small, and callers derive the hint from bounds that hold.

    Order of the entries
    --------------------

    finish() puts the entries in ascending order of pattern code, which is
    what makes a cluster vector reproducible: the elements are sums over the
    entries, and floating point addition is not associative, so the result
    depends on the order in which the entries are visited. Ascending code
    order is the order the patterns themselves compare in, so it does not
    depend on the order in which clusters happened to be counted.
*/
class ClusterCountBuffer
{
public:
    /// One accumulated occupation pattern.
    struct Entry
    {
        /// Encoded occupation pattern, or EMPTY_SLOT in a slot that holds no entry.
        int64_t pattern;

        /// Weight accumulated for that pattern.
        double weight;
    };

    /// Marks a slot that holds no entry; pattern codes are non-negative.
    static constexpr int64_t EMPTY_SLOT = -1;

    /**
    @brief Empties the buffer and makes room for the given number of entries.
    @details
        Pass the largest number of distinct patterns any orbit of the
        evaluation can produce, rather than the number this particular orbit
        can, so that the storage is sized once per call instead of growing
        from orbit to orbit.
    @param maximumDistinctPatterns upper bound on the number of distinct patterns
    */
    void prepare(const size_t maximumDistinctPatterns);

    /**
    @brief Adds a weight to the entry of the given pattern.
    @param pattern encoded occupation pattern of a cluster
    @param weight weight the cluster is counted with
    */
    void add(const int64_t pattern, const double weight)
    {
        size_t slot = (size_t)pattern & _slotMask;
        while (true)
        {
            const int64_t occupant = _slots[slot].pattern;
            if (occupant == pattern)
            {
                _slots[slot].weight += weight;
                return;
            }
            if (occupant == EMPTY_SLOT)
            {
                _slots[slot].pattern = pattern;
                _slots[slot].weight = weight;
                _usedSlots.push_back(slot);
                if (2 * _usedSlots.size() > _slots.size())
                {
                    growAndRehash();
                }
                return;
            }
            slot = (slot + 1) & _slotMask;
        }
    }

    /// Puts the entries in ascending order of pattern code; call once counting is done.
    void finish();

    /// Returns the number of entries, available once finish() has been called.
    size_t size() const { return _entries.size(); }

    /// Returns the pattern code of the entry with the given index.
    int64_t pattern(const size_t index) const { return _entries[index].pattern; }

    /// Returns the accumulated weight of the entry with the given index.
    double weight(const size_t index) const { return _entries[index].weight; }

private:
    /**
    @brief Doubles the capacity and moves the entries into the new table.
    @details
        Reached only when more distinct patterns turned up than prepare()
        was told to expect. The entries keep their accumulated weights, and
        the order they are held in does not matter, since it only decides
        which slots get cleared and finish() sorts before anything reads
        them.

        Defined out of line deliberately, so that add(), which is what the
        counting loops inline, carries only the test that reaches it.
    */
    void growAndRehash();

    /// Bit mask that reduces a pattern code to a slot; capacity minus one.
    size_t _slotMask = 0;

    /// The open-addressing table.
    std::vector<Entry> _slots;

    /// The slots that hold an entry, in the order they were first written.
    std::vector<size_t> _usedSlots;

    /// The entries in ascending order of pattern code, filled by finish().
    std::vector<Entry> _entries;
};
