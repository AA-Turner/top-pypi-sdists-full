from __future__ import unicode_literals

import collections

class ListCrunchError(Exception):
    pass

def crunch_collection(collection):
    parts = []
    for value, nums in sorted(collection.items(), key=lambda x: x[1]):

        subparts = []
        run = None

        def end_run(run):
            if run is None:
                return
            if run[0] == run[1]:
                subparts.append("{}".format(run[0]))
            else:
                subparts.append("{}-{}".format(run[0], run[1]))
        
        for num in nums:
            if run is None:
                run = [num, num]
            else:
                if num == run[1] + 1:
                    run[1] = num
                else:
                    end_run(run)
                    # Start a new run
                    run = [num, num]

        end_run(run)
        joined = ",".join(subparts)
        parts.append("{}:{}".format(value, joined))

    return ";".join(parts)

def crunch(items):
    cruncher = collections.defaultdict(list)
    for num, item in enumerate(items):
        cruncher[item].append(num)
    
    return crunch_collection(cruncher)

def uncrunch(s):
    if len(s.strip()) == 0: return []

    results = []

    parts = s.split(';')
    for part in parts:
        subparts = part.split(':')
        if len(subparts) != 2:
            raise ListCrunchError("Each ';'-delimited region must have exactly one ':'")
        value = subparts[0]
        specs = subparts[1].split(',')

        for spec in specs:
            if '-' in spec:
                # Parse a range
                startEnd = spec.split('-')
                if len(startEnd) != 2:
                    raise ListCrunchError("Each page range (e.g. 3-5) must have exactly one '-'")
                start = int(startEnd[0])
                end = int(startEnd[1])
                for i in range(start, end + 1):
                    results.append([i, value])
            else:
                results.append([int(spec), value])
    
    sorted_results = sorted(results, key=lambda x: x[0])
    nums, values = zip(*sorted_results)
    if list(nums) != list(range(len(results))):
        raise ListCrunchError("Inconsistent results length: this should never happen")
    return list(values)
