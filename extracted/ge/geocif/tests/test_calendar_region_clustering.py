"""Tests for cluster_strategy='crop_calendar_region' — pooling admin regions by
their EXPLICIT crop-calendar zone (the ``calendar_region`` column from crop_t0),
NOT the CID null-pattern proxy used by 'crop_calendar'.

The pure grouping logic lives in ``geocif.utils.group_ids_by_key`` (testable
without importing the heavy geocif.geocif module).
"""
from geocif import utils


def _norm(s):
    return str(s).lower().replace(" ", "_").replace("-", "_")


def test_regions_sharing_zone_get_same_id():
    # Brazil-like: 5 states across 3 zones.
    zone_map = {
        "mato_grosso": "central-west_region",
        "goias": "central-west_region",
        "para": "north_region",
        "bahia": "northeast_region",
        "maranhao": "northeast_region",
    }
    regions = ["Mato Grosso", "Goias", "Para", "Bahia", "Maranhao"]
    ids = utils.group_ids_by_key(regions, zone_map, norm=_norm)
    # Mato Grosso + Goias share a pool; Bahia + Maranhao share a pool.
    assert ids[0] == ids[1]              # central-west
    assert ids[3] == ids[4]              # northeast
    assert ids[2] not in (ids[0], ids[3])  # north distinct
    assert len(set(ids)) == 3            # 3 zones


def test_dense_ids_first_seen_order():
    zone_map = {"a": "z1", "b": "z2", "c": "z1"}
    ids = utils.group_ids_by_key(["a", "b", "c"], zone_map)
    assert ids == [0, 1, 0]              # dense, first-seen


def test_unmatched_region_gets_own_singleton():
    zone_map = {"para": "north_region", "bahia": "northeast_region"}
    regions = ["Para", "Bahia", "Unknown State", "Another Unknown"]
    ids = utils.group_ids_by_key(regions, zone_map, norm=_norm)
    # Unmatched regions never collapse into an existing zone or into each other.
    assert len(set(ids)) == 4
    assert ids[2] != ids[3]
    assert ids[2] not in (ids[0], ids[1])


def test_brazil_27_states_5_zones():
    # Full Brazil soybean zone map (matches crop_t0 calendar_region).
    zones = {
        "central-west_region": ["distrito_federal", "goias", "mato_grosso", "mato_grosso_do_sul"],
        "north_region": ["acre", "amapa", "amazonas", "para", "rondonia", "roraima", "tocantins"],
        "northeast_region": ["alagoas", "bahia", "ceara", "maranhao", "paraiba",
                             "pernambuco", "piaui", "rio_grande_do_norte", "sergipe"],
        "south_region": ["parana", "rio_grande_do_sul", "santa_catarina"],
        "southeast_region": ["espirito_santo", "minas_gerais", "rio_de_janeiro", "sao_paulo"],
    }
    zone_map = {r: z for z, rs in zones.items() for r in rs}
    regions = [r for rs in zones.values() for r in rs]
    ids = utils.group_ids_by_key(regions, zone_map, norm=_norm)
    assert len(regions) == 27
    assert len(set(ids)) == 5


if __name__ == "__main__":
    import sys, pytest
    sys.exit(pytest.main([__file__, "-v"]))
