from .imports import *
from .update_utils import *
def get_all_attribute_values(keys,attributes=None,*args,  **kwargs):
    """
    Extract all values for given attribute(s) from tags.
    
    Works with:
        • Direct list of BeautifulSoup tags
        • A criteria dict/string (will call find_attribs internally)
        • soup_mgr, url, source_code passed via *args/**kwargs
    
    Examples:
        get_all_attribute_values(last_page_span, "onclick")
        get_all_attribute_values(last_page_span, ["onclick", "title"])
        get_all_attribute_values({"span": {"title": "Last Page"}}, "onclick", url=...)
    """
    # Step 1: Resolve input → list of Tag objects
    tags = find_attribs(attributes, *args, **kwargs)
    
    if not tags:
        return {}
    result={}
    # Step 2: Normalize attributes to list
    attributes = make_list(attributes) if attributes is not None else []
    for tag in tags:
        for key in keys:
            val = tag.get(key)
            if val is not None:
                if key not in result:
                    result[key]=[]
                result[key].append(val)
    return result
def get_soup_mgr(*args,**kwargs):
    soup_mgr,_ = make_mgr_updates(*args,**kwargs)
    return soup_mgr or soupManager(*args,**kwargs)
def find_attribs(attribs,*args,**kwargs):
    soup_mgr = get_soup_mgr(*args,**kwargs)
    return soup_mgr.findit(attribs)
def find_attr_values(keys,attributes,*args,**kwargs):
    soup_mgr = get_soup_mgr(*args,**kwargs)
    return get_all_attribute_values(make_list(keys), attributes=attributes, soup_mgr=soup_mgr)
