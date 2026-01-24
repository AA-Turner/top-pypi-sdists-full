def normalize_page_args(kwargs):
    page_sort = kwargs.get("page_sort")
    if isinstance(page_sort, tuple):
        kwargs["page_sort"] = list(page_sort)
    page_on = kwargs.get("page_on")
    if isinstance(page_on, tuple):
        kwargs["page_on"] = list(page_on)
    return kwargs
