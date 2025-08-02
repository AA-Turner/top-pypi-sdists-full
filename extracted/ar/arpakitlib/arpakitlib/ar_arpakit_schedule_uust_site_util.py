# arpakit

from urllib.parse import urlencode, urljoin

from arpakitlib.ar_type_util import raise_for_type

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def generate_arpakit_schedule_uust_site_url(
        *,
        base_url: str = "https://schedule-uust.arpakit.com",
        entity_type: str | None = None,
        uust_api_id: int | None = None,
        session: bool | None = None,
        week: int | None = None,
        theme: str | None = None
) -> str:
    raise_for_type(base_url, str)

    params = {}

    if entity_type is not None:  # group/teacher
        raise_for_type(entity_type, str)
        params["entity_type"] = entity_type

    if uust_api_id is not None:  # uust_api_id of group/teacher
        raise_for_type(uust_api_id, int)
        params["uust_api_id"] = uust_api_id

    if session is not None:  # true/false
        raise_for_type(session, bool)
        if session:
            params["session"] = "true"
        else:
            params["session"] = "false"

    if week is not None:
        raise_for_type(week, int)
        params["week"] = week

    if theme is not None:  # dark/light
        raise_for_type(theme, str)
        params["theme"] = theme

    if params:
        res = urljoin(base_url, f"schedule?{urlencode(params)}")
    else:
        res = base_url

    return res


def __example():
    base_url = "https://schedule-uust.arpakit.com"
    url = generate_arpakit_schedule_uust_site_url(
        base_url=base_url,
        entity_type="group",
        uust_api_id=6662,
        session=True,
        week=23,
        theme="dark"
    )
    print(url)


if __name__ == '__main__':
    __example()
