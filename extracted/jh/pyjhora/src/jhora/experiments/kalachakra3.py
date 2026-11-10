#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright (C) Open Astro Technologies, USA.
# Modified by Sundar Sundaresan, USA. carnaticmusicguru2015@comcast.net
# Downloaded from https://github.com/naturalstupid/PyJHora

# This file is part of the "PyJHora" Python library
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
    Compute Rashiyanka/Rasyamsaka Dhasa - Ref: https://astrologicalmusings.com/method-of-calculating-rashiyanka-dasha/
"""
from jhora import const, utils
from jhora.horoscope.chart import charts, house
from jhora.panchanga import drik

# Module-level year basis. Public entry points refresh this via drik.dhasa_year_duration().
year_duration = const.sidereal_year


def _set_year_duration(jd, place, dhasa_duration_type=None, savana_year_method=None):
    global year_duration
    year_duration = drik.dhasa_year_duration(
        jd=jd,
        place=place,
        dhasa_duration_type=dhasa_duration_type,
        savana_year_method=savana_year_method,
    )
    return year_duration


def applicability(pp_d1):
    # lagna lord in exaltion, own or friends house
    asc_d1 = pp_d1[0][1][0]
    lord_asc_d1 = house.house_owner_from_planet_positions(pp_d1, asc_d1)
    house_lord_asc_d1 = pp_d1[lord_asc_d1 + 1][1][0]
    return utils.is_planet_strong(lord_asc_d1, house_lord_asc_d1)


def _dhasa_progression(jd_at_dob, place, divisional_chart_factor=9,
                       dhasa_progression_method=None,chart_method=1):
    """
        Dhasa progression direct in both cases
        dhasa method = 1 BPHS Venkateshwar Edition (Translator: Pandit Tara Chand Shastri)
            starts from navamsa rasi of rasi lagna lord
        dhasa method = 2 BPHS - (Translator: Pandit Ganesh Dutt Pathak)
            starts from navamsa rasi of rasi lagna lord
    """
    if dhasa_progression_method is None: dhasa_progression_method = const.rasyamsaka_dhasa_method_default
    pp_rasi = charts.rasi_chart(jd_at_dob,place)
    pp_varga = charts.divisional_chart(jd_at_dob, place, divisional_chart_factor=divisional_chart_factor,
                                       chart_method=chart_method)
    asc_d1 = pp_rasi[0][1][0]
    lord_asc = const._house_owners_list[asc_d1]  # force Parāśari lords
    asc_varga = pp_varga[0][1][0]
    lord_asc_varga = pp_varga[lord_asc + 1][1][0]

    if dhasa_progression_method == const.RASYAMSAKA_METHOD.VENKATESHWAR_BPHS:
        seed = lord_asc_varga  # Venkateśvara: Lagna-lord' sign in Varga chart
    else:
        # Pathak: stronger(Lagna, Lagna-lord) in D-1 → take that entity’s varga chart sign
        stronger_in_d1 = house.stronger_rasi_from_planet_positions(
            pp_rasi, asc_d1, pp_rasi[lord_asc + 1][1][0]
        )
        seed = asc_varga if stronger_in_d1 == asc_d1 else lord_asc_varga

    return [(seed + h) % 12 for h in range(12)]

def _dhasa_duration(pp_varga, sign):
    p_to_h_varga = utils.get_planet_house_dictionary_from_planet_positions(pp_varga)
    lord_of_sign = const._house_owners_list[sign]
    house_of_lord = p_to_h_varga[lord_of_sign]
    direction = 1 if sign in const.odd_signs else -1
    return utils.count_rasis(from_rasi=sign,to_rasi=house_of_lord,direction=direction)
def get_dhasa_antardhasa(
    dob, tob, place,
    divisional_chart_factor=9,
    dhasa_level_index=const.MAHA_DHASA_DEPTH.ANTARA,              # 1..6 (1=Maha only, 2=Bhukti, 3..6 deeper)
    dhasa_method=None,       # 1=BPHS (Tara Chand Shastri), 2=BPHS (Ganesh Dutt Pathak)
    chart_method=1,                   # chart method for Dx
    round_duration=True,              # only the returned duration (display) is rounded
    dhasa_duration_type=None,
    savana_year_method=None,
    **kwargs
):
    """
    Rāśyāṁśaka / Rāśiyanka Daśā (depth-enabled, 1..6).

    RETURNS (canonical flat list), each row shaped as:
      ( (L1, ..., Lk), (y,m,d,float_hours), dur_years_float )

    Mechanics:
      • Progression order (seed & cycle of 12): _dhasa_progression(...)
      • Durations per sign: _dhasa_duration(planet_positions, sign, dhasa_duration_method)
      • L1 (Maha) uses raw years; L2..N sublevels:
          - "equal"        → split parent equally into 12
          - "proportional" → scale raw 12-sign durations to exactly fill the parent
      • All JD arithmetic uses module-level year_duration.
      • Only the returned 'dur_years' is optionally rounded (display).
    """
    if dhasa_method is None: dhasa_method = const.rasyamsaka_dhasa_method_default
    # ── 0) Validate depth & set rounding precision ───────────────────────────
    lvl = int(dhasa_level_index)
    if not (1 <= lvl <= 6):
        raise ValueError("dhasa_level_index must be in 1..6")
    ndigits = lvl if round_duration else None

    # ── 1) Epoch & chart ─────────────────────────────────────────────────────
    jd_birth = utils.julian_day_number(dob, tob)
    _set_year_duration(jd_birth, place, dhasa_duration_type, savana_year_method)
    pp_varga = charts.divisional_chart(jd_at_dob, place,
                                       divisional_chart_factor=divisional_chart_factor,
                                       chart_method=chart_method,**kwargs)
    # ── 1) Progression cycle of 12 (seeded order) ────────────────────────────
    maha_lord_sequence = _dhasa_progression(
        jd_at_dob, place,divisional_chart_factor=divisional_chart_factor,
        dhasa_progression_method=dhasa_method,
        chart_method=chart_method,
        **kwargs
    )
    start_jd = jd_at_dob
    db = []
    for maha_lord in maha_lord_sequence:
        md_duration = _dhasa_duration(pp_varga,maha_lord)
        end_jd = drik._get_dhasa_end_jd(start_jd,place,md_duration)
        db.append([(maha_lord,),utils.jd_to_gregorian(start_jd),md_duration])
        start_jd = end_jd
    return db
if __name__ == "__main__":
    utils.set_language('en')
    chart1_dob = drik.Date(1953, 5, 6)
    chart1_tob = (6, 10, 0)
    chart1_place = drik.Place('Tony Blair,Edinburgh,Scotland', 55+57/60, -3-13/60, +1.0)
    jd_at_dob = utils.julian_day_number(chart1_dob, chart1_tob)
    db = get_dhasa_antardhasa(chart1_dob, chart1_tob, chart1_place)
    for (lord,),start,durn in db:
        lord_str = utils.RAASI_LIST[lord]
        start_str = f"{start[0]}-{start[1]}-{start[2]} {utils.to_dms(start[3])}"
        print(f"{lord_str} {start_str} {durn} years")
    exit()
