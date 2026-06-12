
from ..imports import *
from .title_variants import title_variants_from_domain
def sort_longest_first(values):
    seen = set()
    clean = []
    for v in values:
        if v and isinstance(v, str):
            low = v.lower()
            if low not in seen:
                clean.append(v)
                seen.add(low)
    return sorted(clean, key=lambda s: (-len(s), s.lower()))

def get_next_variant(variants,post_js=None):
    post_js = post_js or {}
    key = None
    return_item=None
    if post_js:
        keys = ["page","name","domain"]
        for key in keys:
            item = post_js.get(key)
            if item:
                return_item = item
                break
    if key and key in post_js:
        del post_js[key]
    if not return_item and variants:
        return_item = variants.pop()
    return return_item,post_js,variants
def get_all_title_variants(variants=None,page=None,name=None,domain=None):
    variants = variants or []
    title_variants=[]
    post_js = {"page":page,"name":name,"domain":domain}
    variants = sort_longest_first(list(set(variants)))
    while True:
        variant,post_js,variants = get_next_variant(variants=variants,post_js=post_js)
        if variant not in title_variants:
            title_variants.append(variant)
        if len(variants) == 0 and len(post_js) == 0:
            break
    return title_variants
def truncate_or_add(string,size_range,title_variants=None,domain = None,page=None,name=None):
    string_len = len(string)
    min_range = size_range.get('min')
    max_range = size_range.get('max')
    min_len_min = min_range[0]
    min_len_max = min_range[1]
    max_len_min = max_range[0]
    max_len_max = max_range[1]
    title_variants = get_all_title_variants(variants=title_variants,page=page,name=name,domain=domain)
    all_range = [min_len_min,max_len_max]
    in_all_range = is_string_in_range(string, all_range)
    if not in_all_range:
        if string_len < min_len_min:
            need_len = [min_len_min - string_len,min_len_max - string_len]
            
            while True:
                title_variant,post_js,title_variants = get_next_variant(variants=title_variants)
                add_variant=''
                if string:
                    add_variant += ' | '
                add_variant += f"{title_variant}"
                if add_variant not in string and title_variant not in string:
                    add_variant_len = len(add_variant)
                    if add_variant_len <= need_len[-1]:
                        string+= add_variant
                        need_len = [need_len[0] - add_variant_len,need_len[1] - add_variant_len]
                if len(title_variants) == 0:
                    break
            
        else:
            string = truncate_text(string,max_len_max)#[string_len - max_len_min,string_len - max_len_max]
    return string
def get_keywords(info,page=None,domain=None,name=None):
    keywords = info.get('keywords', [])
    keywords_str = info.get('keywords_str', '')
    variants = info.get("title_variants")
    title_variants=get_all_title_variants(variants=variants,page=page,name=name,domain=domain)
    if keywords_str and not keywords:
        keywords = make_list(keywords_str.split(','))
    if keywords and not keywords_str:
        keywords_str = ','.join(keywords)
    if not keywords and not keywords_str:
        keywords = title_variants
        keywords_str = ','.join(keywords)
    if len(keywords) < 10:
        keywords = title_variants
        keywords = [keyword.replace(' ','_') for keyword in keywords if keyword and '|' not in keyword]
        keywords_len = len(keywords)
        if keywords_len >10:
            keywords_len = 10
        keywords = keywords[:keywords_len]
        keywords_str = ','.join(keywords)
    return {"keywords":keywords,"keywords_str":keywords_str} 
def get_title(info):
    title = info.get('title')
    if not title:
        path = info.get('path')
        paths = [pa for pa in path.split('/') if pa]
        title = paths[-1] if len(paths)>0 else ''
        if title == '':
            title = 'Home'
    return title
def is_string_in_range(s, size_range):
    if not isinstance(s, str):
        return False
    return size_range[0] <= len(s.strip()) <= size_range[1]

def get_max_or_limit(obj, limit=None):
    if limit and len(obj) >= limit:
        return obj[:limit]
    return obj

def title_add(current_string="", size_range=None):
    if not size_range or not isinstance(current_string, str):
        return current_string

    result = current_string.strip()
    min_len, max_len = size_range

    if is_string_in_range(result, size_range):
        return result

    potentials = title_variants_from_domain(result)
    sep = " | "

    for pot in potentials:
        candidate = result + sep + pot
        if len(candidate) <= max_len:
            result = candidate
            break

    while len(result) < min_len and len(result) < max_len:
        for pot in reversed(potentials):
            candidate = result + sep + pot
            if len(candidate) <= max_len:
                result = candidate
            else:
                break

    parts = result.split("|")
    parts = get_max_or_limit(parts, limit=3)
    return "|".join(parts).strip()

def pad_or_trim(typ, string, platform=None, title_variants=None,domain = None,page=None,name=None):

    if not isinstance(string, str):
        return ""

    string = string.strip()
    limits = META_VARS.get(typ, {"max": [0, float('inf')]})
    max_range = limits["max"]

    if platform == "twitter":
        if typ == "title": max_range = [60, 70]
        if typ == "description": max_range = [150, 200]

    elif platform == "og":
        if typ == "title":
            max_range = [60, 90]
            if len(string) > 100: return string[:88].strip()
        if typ == "description":
            max_range = [150, 200]
            if len(string) > 300: return string[:300].strip()
    return truncate_or_add(string=string,size_range=limits,title_variants=title_variants,domain = domain,page=page,name=name)
