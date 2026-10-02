#include "ClusterCountBuffer.hpp"

/*
Everything here runs once per orbit or less, never per cluster, which is why
it is defined out of line: the counting loops inline add() and should carry
nothing else.
*/

void ClusterCountBuffer::prepare(const size_t maximumDistinctPatterns)
{
    size_t capacity = 8;
    while (capacity < 2 * maximumDistinctPatterns)
    {
        capacity *= 2;
    }
    if (capacity > _slots.size())
    {
        _slots.assign(capacity, Entry{EMPTY_SLOT, 0.0});
        _slotMask = capacity - 1;
        // Room for an entry per slot is more than the half-full guarantee
        // needs, but it makes the reservation independent of which orbit the
        // buffer is prepared for first.
        _usedSlots.reserve(capacity);
        _entries.reserve(capacity);
    }
    else
    {
        for (const size_t slot : _usedSlots)
        {
            _slots[slot].pattern = EMPTY_SLOT;
        }
    }
    _usedSlots.clear();
    _entries.clear();
}

void ClusterCountBuffer::finish()
{
    std::sort(_usedSlots.begin(), _usedSlots.end(),
              [this](const size_t left, const size_t right)
              { return _slots[left].pattern < _slots[right].pattern; });
    for (const size_t slot : _usedSlots)
    {
        _entries.push_back(_slots[slot]);
    }
}

void ClusterCountBuffer::growAndRehash()
{
    std::vector<Entry> held;
    held.reserve(_usedSlots.size());
    for (const size_t slot : _usedSlots)
    {
        held.push_back(_slots[slot]);
    }
    const size_t capacity = 2 * _slots.size();
    _slots.assign(capacity, Entry{EMPTY_SLOT, 0.0});
    _slotMask = capacity - 1;
    _usedSlots.clear();
    _usedSlots.reserve(capacity);
    _entries.reserve(capacity);
    for (const Entry &entry : held)
    {
        size_t slot = (size_t)entry.pattern & _slotMask;
        while (_slots[slot].pattern != EMPTY_SLOT)
        {
            slot = (slot + 1) & _slotMask;
        }
        _slots[slot] = entry;
        _usedSlots.push_back(slot);
    }
}
