"""
subdivideIntervalsInTier() will split all intervals in a named tier X number of times.

Each interval will have the same label as the source interval's label.
"""

from praatio import textgrid


def subdivide(start, end, numDivisions):
    duration = end - start
    fragmentDuration = duration / float(numDivisions)
    entries = []
    for _ in range(numDivisions):
        entries.append([start, start + fragmentDuration])
        start += fragmentDuration

    return entries


def subdivideIntervalsInTier(fn, outputFn, tierName, numDivisions):
    tg = textgrid.openTextgrid(fn, False)
    tier = tg.getTier(tierName)

    newEntries = []
    for interval in tier.entries:
        entries = subdivide(interval.start, interval.end, numDivisions)
        entries = [[start, end, interval.label] for start, end in entries]
        newEntries.extend(entries)
    replTier = tier.new(entries=newEntries)
    tg.replaceTier(tierName, replTier)
    tg.save(outputFn, "short_textgrid", True)


if __name__ == "__main__":

    fn = "files/mary.TextGrid"
    outputFn = "files/mary_subdivided.TextGrid"
    subdivideIntervalsInTier(fn, outputFn, "word", 4)
