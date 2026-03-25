import math
import re
from itertools import count as itercount
from itertools import takewhile

import colour


def interpolate_color(color1, color2, ratio):
    if ratio < 0:
        ratio = 0
    elif ratio > 1:
        ratio = 1
    c1 = colour.Color(color1)
    c2 = colour.Color(color2)
    c3 = colour.Color(
        hue=((1 - ratio) * c1.hue + ratio * c2.hue),
        saturation=((1 - ratio) * c1.saturation + ratio * c2.saturation),
        luminance=((1 - ratio) * c1.luminance + ratio * c2.luminance),
    )
    return c3.hex_l


def build_level_colors(track_color, special_color1=None, special_color2=None):
    """
    Build four positive contribution shades for a five-level heatmap.
    """
    level1 = interpolate_color(track_color, "#ffffff", 0.35)
    if special_color1 and special_color2:
        level2 = interpolate_color(track_color, special_color1, 0.35)
        return [level1, level2, special_color1, special_color2]

    level2 = track_color
    level3 = interpolate_color(track_color, "#000000", 0.18)
    level4 = interpolate_color(track_color, "#000000", 0.35)
    return [level1, level2, level3, level4]


def parse_years(s):
    """Parse a plaintext range of years into a pair of years

    Attempt to turn the input string into a pair of year values, from_year and to_year.
    If one year is passed, both from_year and to_year will be set to that year.
    If a range like '2016-2018' is passed, from_year will be set to 2016,
    and to_year will be set to 2018.

    Args:
        s: A string representing a range of years or a single year
    """
    m = re.match(r"^\d+$", s)
    if m:
        from_year = int(s)
        to_year = from_year
        return from_year, to_year
    m = re.match(r"^(\d+)-(\d+)$", s)
    if m:
        y1, y2 = int(m.group(1)), int(m.group(2))
        if y1 <= y2:
            from_year = y1
            to_year = y2
        else:
            from_year = y2
            to_year = y1
    return from_year, to_year


def make_key_times(year_count):
    """
    year_count: year run date count
    return: list of key times points
    should append `1` because the svg keyTimes rule
    """
    s = list(takewhile(lambda n: n < 1, itercount(0, 1 / year_count)))
    s.append(1)
    return [str(round(i, 2)) for i in s]


def make_github_level_thresholds(number_list):
    """
    GitHub exposes contribution levels as NONE plus four quartiles.
    This uses the non-zero daily values and a nearest-rank percentile.
    """
    positive_values = sorted(v for v in number_list if v > 0)
    if not positive_values:
        return ()

    total = len(positive_values)

    def nearest_rank(percentile):
        index = max(0, math.ceil(total * percentile) - 1)
        return positive_values[index]

    return tuple(nearest_rank(p) for p in (0.25, 0.50, 0.75))


def resolve_github_level(value, thresholds):
    if value <= 0:
        return 0
    if not thresholds:
        return 1

    q1, q2, q3 = thresholds
    if value <= q1:
        return 1
    if value <= q2:
        return 2
    if value <= q3:
        return 3
    return 4


def reduce_year_list(year_list, tracks_dict):
    """
    format year list
    [2012, 2013, 2014, 2015, 2016]
    if 2012, 2013 values are 0
    year list to [2013, 2015, 2016]
    """
    year_list_keys = list(tracks_dict.keys())
    year_list_keys.sort()
    s = set()
    for key in year_list_keys:
        if tracks_dict.get(key, 0) > 0:
            s.add(key[:4])
    year_list.sort()
    i = 0
    for year in year_list:
        if str(year) not in s:
            i += 1
        else:
            break
    return year_list[i:]
