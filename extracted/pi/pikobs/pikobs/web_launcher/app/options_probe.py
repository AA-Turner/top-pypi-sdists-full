#!/usr/bin/env python3
"""Return selectable values from the Pikobs installed in this interpreter.

This module is launched in a fresh process by Pikobs Web. A fresh interpreter
is important because a user may run ``pikobs-update`` while the web server is
already alive; the child process then sees the updated environment without a
Pikobs Web reinstall or server restart.

Besides the flat family list, the probe returns a presentation catalogue for
Pikobs Web. The catalogue explains how a logical observation family appears
through the data chain (postalt -> bgckalt -> evalalt -> derialt -> cutoff ->
dbase). Stage and instrument names are presentation only. Only values already
recognised by the installed ``pikobs.configobs.families`` are selectable.
"""
from __future__ import annotations

import importlib
import inspect
import json
import re
from importlib.metadata import PackageNotFoundError, version


STAGE_ORDER = ("postalt", "bgckalt", "evalalt", "derialt", "cutoff", "dbase")

# Fallback copy of the chain documented by pikobs.configobs.families. The
# installed CSV/documentation remains authoritative when available; these
# rows only keep the web useful with an older installed Pikobs.
CHAIN_ROWS = [
    ("ua", "Radiosondes", {
        "cutoff": ["ua_cmc", "ua_radiosonde", "ua_radiosonde_b"],
        "derialt": ["ua", "ua_a", "ua_b"], "evalalt": ["ua_qc"],
        "bgckalt": ["ua"], "postalt": ["ua"],
        "dbase": ["uprair/radiosonde", "uprair/radiosonde_b"],
    }),
    ("ai", "Aircraft", {
        "cutoff": ["ai_acars", "ai_ads", "ai_airep", "ai_amdar"],
        "derialt": ["ai"], "evalalt": ["ai_qc"], "bgckalt": ["ai"], "postalt": ["ai"],
        "dbase": ["uprair/acars", "uprair/amdar", "uprair/airep", "uprair/ads"],
    }),
    ("sf", "Surface", {
        "cutoff": ["sf_synop", "sf_synop_b", "sf_metar", "sf_awos", "sf_hwos", "sf_ca", "sf_drifter", "sf_drifter_b", "sf_winide"],
        "derialt": ["sf", "sf_a", "sf_b", "sf2", "sf2_a", "sf2_b"], "evalalt": ["sf_qc"],
        "bgckalt": ["sf"], "postalt": ["sf"],
        "dbase": ["surface/synop", "surface/synop_b", "surface/metar", "swob/ca", "swob/winide", "swob/nchwos", "swob/ncawos", "swob/non/bcforest", "swob/non/cocorahs", "swob/non/bctran", "swob/non/mnr", "swob/non/trca", "swob/non/grca"],
    }),
    ("sc", "Scatterometers", {
        "cutoff": ["sc_ascat", "sc_hscat"], "derialt": ["sc"], "evalalt": ["sc_qc"],
        "bgckalt": ["sc"], "postalt": ["sc"], "dbase": ["remote/ascat", "remote/hscat"],
    }),
    ("sw", "Satellite winds (AMV)", {
        "cutoff": ["sw_geo", "sw_polar"], "derialt": ["sw"], "evalalt": ["sw_qc", "sw_polaireDB_qc"],
        "bgckalt": ["sw", "sw_polaireDB"], "postalt": ["sw", "sw_polaireDB"],
        "dbase": ["remote/satwinds/geo", "remote/satwinds/polar"],
    }),
    ("ro", "GNSS radio occultation", {
        "cutoff": ["ro"], "derialt": ["ro"], "evalalt": ["ro_qc"], "bgckalt": ["ro"], "postalt": ["ro"],
        "dbase": ["remote/gpsocc"],
    }),
    ("gp", "Ground-based GPS", {
        "cutoff": ["gp", "gp_b"], "derialt": ["gp", "gp2"], "evalalt": ["gp_qc"], "bgckalt": ["gp"], "postalt": ["gp"],
        "dbase": ["remote/gpssfc", "remote/gpssfc_b"],
    }),
    ("pr", "Wind profilers", {"cutoff": ["pr"], "dbase": ["uprair/profiler"]}),
    ("ch", "Ozone / chemistry", {
        "cutoff": ["ch_gome", "ch_omps_np", "ch_omps_tc", "tar_ch_mlso3", "tar_ch_omto3", "tar_ch_tropomi"],
        "derialt": ["ch_o3_gome2b", "ch_o3_mls", "ch_o3_omi", "ch_o3_ompsnm", "ch_o3_ompsnmb", "ch_o3_ompsnmc", "ch_o3_ompsnp", "ch_o3_tropomi"],
        "bgckalt": ["ch"], "postalt": ["ch"],
        "dbase": ["derialt/ch/gome2b", "derialt/ch/mls", "derialt/ch/omi", "derialt/ch/ompsnm", "derialt/ch/ompsnmb", "derialt/ch/ompsnmc", "derialt/ch/ompsnp", "derialt/ch/tropomi"],
    }),
    ("to_amsua", "Microwave radiances - AMSU-A", {
        "cutoff": ["to_amsua", "rars_amsua"], "derialt": ["to_amsua", "rars_amsua"],
        "evalalt": ["to_amsua_qc", "to_amsua_allsky_qc", "to_amsua_allsky_rars_qc"],
        "bgckalt": ["to_amsua", "to_amsua_allsky", "to_amsua_allsky_rars"],
        "postalt": ["to_amsua_allsky", "to_amsua_allsky_rars"],
        "dbase": ["remote/tovs1b/amsua", "remote/rars/amsua"],
    }),
    ("to_amsub", "Microwave radiances - AMSU-B / MHS", {
        "cutoff": ["to_amsub", "rars_amsub"], "derialt": ["to_amsub", "rars_amsub"],
        "evalalt": ["to_amsub_qc", "to_amsub_allsky_qc", "to_amsub_allsky_rars_qc"],
        "bgckalt": ["to_amsub", "to_amsub_allsky", "to_amsub_allsky_rars"],
        "postalt": ["to_amsub_allsky", "to_amsub_allsky_rars"],
        "dbase": ["remote/tovs1b/mhs", "remote/rars/mhs"],
    }),
    ("atms", "Microwave radiances - ATMS", {
        "cutoff": ["atms", "rars_atms"], "derialt": ["atms", "rars_atms"],
        "evalalt": ["atms_qc", "atms_allsky_qc"], "bgckalt": ["atms", "atms_allsky"],
        "postalt": ["atms_allsky"], "dbase": ["remote/atms"],
    }),
    ("mwhs2", "Microwave radiances - MWHS-2", {
        "cutoff": ["mwhs2", "rars_mwhs2"], "derialt": ["mwhs2", "rars_mwhs2"],
        "evalalt": ["mwhs2_qc", "mwhs2_rars_qc"], "bgckalt": ["mwhs2", "mwhs2_rars"],
        "postalt": ["mwhs2", "mwhs2_rars"], "dbase": ["remote/rars/mwhs2"],
    }),
    ("ssmis", "Microwave radiances - SSMIS", {
        "cutoff": ["ssmis"], "derialt": ["ssmis"], "evalalt": ["ssmis_qc"], "bgckalt": ["ssmis"], "postalt": ["ssmis"],
        "dbase": ["remote/ssmis"],
    }),
    ("iasi", "Infrared radiances - IASI", {
        "cutoff": ["iasi"], "derialt": ["iasi"], "evalalt": ["iasi_qc"], "bgckalt": ["iasi"], "postalt": ["iasi"],
        "dbase": ["remote/iasi"],
    }),
    ("cris", "Infrared radiances - CrIS", {
        "cutoff": ["crisfsr"], "derialt": ["crisfsr"], "evalalt": ["crisfsr1_qc", "crisfsr2_qc"],
        "bgckalt": ["cris"], "postalt": ["cris"], "dbase": ["remote/crisfsr"],
    }),
    ("csr", "Geostationary radiances - CSR", {
        "cutoff": ["csr"], "derialt": ["csr"], "evalalt": ["csr_qc"], "bgckalt": ["csr"], "postalt": ["csr"],
        "dbase": ["remote/csr"],
    }),
    ("asr", "ASR", {"cutoff": ["asr"], "derialt": ["asr"]}),
]


def _family_catalog(recognised: list[str]) -> dict:
    known = {str(x).lower(): str(x) for x in recognised}
    stages = []
    seen_selectable = set()

    for stage in STAGE_ORDER:
        groups = []
        for canonical, label, chain in CHAIN_ROWS:
            suffixes = list(chain.get(stage, []))
            if not suffixes:
                continue
            selectable = []
            for suffix in suffixes:
                if suffix.lower() in known:
                    selectable.append(known[suffix.lower()])
            # cutoff/dbase describe network/file endings that are often not
            # accepted as FAMILY. Keep the logical family selectable instead
            # while showing the exact endings as reference information.
            if not selectable and canonical.lower() in known:
                selectable = [known[canonical.lower()]]
            selectable = list(dict.fromkeys(selectable))
            seen_selectable.update(x.lower() for x in selectable)
            groups.append({
                "family": canonical,
                "instrument": label,
                "values": selectable,
                "suffixes": suffixes,
            })
        stages.append({"id": stage, "label": stage.capitalize(), "groups": groups})

    extras = [x for x in recognised if str(x).lower() not in seen_selectable]
    return {"stage_order": list(STAGE_ORDER), "stages": stages, "extras": extras}


def main() -> None:
    out = {
        "families": [],
        "family_catalog": {"stage_order": list(STAGE_ORDER), "stages": [], "extras": []},
        "regions": [],
        "flags_criteria": [],
        "projections": [],
        "pikobs_version": "",
        "pikobs_path": "",
    }

    try:
        import pikobs
        out["pikobs_path"] = str(getattr(pikobs, "__file__", "") or "")
        try:
            out["pikobs_version"] = version("pikobs")
        except PackageNotFoundError:
            out["pikobs_version"] = str(getattr(pikobs, "__version__", "") or "")
    except Exception:
        pass

    try:
        from pikobs.configobs.families import families
        out["families"] = sorted(dict.fromkeys(str(x) for x in families()))
    except Exception:
        pass
    out["family_catalog"] = _family_catalog(out["families"])

    try:
        from pikobs.configobs import regionsobs
        out["regions"] = sorted(dict.fromkeys(str(x) for x in regionsobs.list_regions()))
    except Exception:
        pass

    try:
        from pikobs.configobs.flags_criteria import flag_criteria
        src = inspect.getsource(flag_criteria)
        names = re.findall(r"(?:if|elif)\s+flags\s*==\s*['\"]([^'\"]+)['\"]", src)
        out["flags_criteria"] = list(dict.fromkeys(names))
    except Exception:
        pass

    try:
        module = importlib.import_module("pikobs.configobs.type_projection")
        rows = getattr(module, "_projection_rows", None)
        values = []
        if callable(rows):
            try:
                values = [
                    str(row[0]).lower()
                    for row in rows()
                    if row and str(row[0]).upper() != "PROJECTION"
                ]
            except Exception:
                values = []
        if not values:
            doc = getattr(module, "__doc__", "") or ""
            names = re.findall(r"\* - ``([A-Za-z0-9_]+)``", doc)
            values = [x.lower() for x in names if x.upper() != "PROJECTION"]
        out["projections"] = list(dict.fromkeys(values))
    except Exception:
        pass

    print(json.dumps(out, sort_keys=True))


if __name__ == "__main__":
    main()
