from stactools.met_office_deterministic.href import Href


def test_hrefs(hrefs: list[str]) -> None:
    for raw_href in hrefs:
        href = Href.parse(raw_href)
        href.item_id.startswith("20250614T")


def test_no_variable() -> None:
    href = Href.parse(
        "http://stactools-met-office-deterministic.test/global-deterministic-10km/20250614T0000Z/20250614T0000Z-PT0000H00M-height_of_orography.nc"
    )
    assert href.variable is None
