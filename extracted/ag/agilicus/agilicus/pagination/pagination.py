import inspect

from typing import Callable


def _make_empty_callback(page_callback):
    return lambda page: page_callback()


def _make_callback_with_page(page_callback):
    return lambda page: page_callback(page)


def get_many_entries(
    api_func: Callable,
    response_list_key,
    page_size=100,
    maximum=None,
    page_callback=None,
    page_key="page_at_id",
    **kwargs,
):
    """Implements the generic pagination strategy
    :param agilicus_api api: api used to get the object
    :param string response_list_key: key to get the value/list from the returned object
    :param int page_size: size of the pagination
    :param int maximum: the maximum number of objects to return. Returns all if None

    Assumes page_at_id is in the kwargs
    """
    if "limit" in kwargs:
        del kwargs["limit"]
    kwargs["limit"] = page_size
    if page_key not in kwargs:
        kwargs[page_key] = ""

    retval = []
    page_callback_wrapper = None
    if page_callback:
        page_callback_wrapper = _make_empty_callback(page_callback)

        args = inspect.getfullargspec(page_callback)
        if "page" in args.args or "page" in args.kwonlyargs:
            page_callback_wrapper = _make_callback_with_page(page_callback)

    def apply_page(page):
        retval.extend(page)

        if page_callback_wrapper:
            page_callback_wrapper(page)

    list_resp = api_func(**kwargs)
    page_items = list_resp.get(response_list_key) or []
    apply_page(page_items)

    # loop quits when the list is < the page_size
    while len(list_resp.get(response_list_key, [])) >= page_size and _list_at_max_size(
        len(retval), maximum
    ):
        page_at_id = list_resp.get(page_key, None)
        if page_at_id is None:
            raise Exception(
                f"{page_key} cannot be None for pagination to continue processing"
            )
        kwargs[page_key] = list_resp.get(page_key, None)
        list_resp = api_func(**kwargs)
        page_items = list_resp.get(response_list_key, [])
        apply_page(page_items)

    return _get_max_retval(retval, maximum)


def _list_at_max_size(length, maximum):
    if maximum is None:
        return True
    return length < maximum


def _get_max_retval(retval, maximum):
    if maximum is None:
        return retval
    return retval[:maximum]
