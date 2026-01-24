from .get_strip_utils import *
from .correct_url_utils import *
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

def get_parsed_url(domain, **kwargs):
    parsed_url = dict(kwargs)
    post_variants = []
    # http / www
    http_www = get_http_www(domain)
    parsed_url.update(http_www)

    http = http_www.get('http')

    # basic domain pieces
    domain_paths = get_domain_paths(domain, http=http)
    parsed_url.update(domain_paths)

    domain_name_ext = get_domain_name_ext(domain, http=http)
    parsed_url.update(domain_name_ext)

    domain_name = parsed_url.get('name')
    domain = parsed_url.get('domain')
        # tokenization
    tokenized_domain = tokenize_domain(domain)
    parsed_url["tokenized_domain"] = tokenized_domain
    app_name = " ".join(tokenized_domain)
    parsed_url["app_name"] = app_name
    


  



    # author / "i_url"
    parsed_url["author"] = f"@{domain_name.lower()}"
    parsed_url["i_url"] = f"{domain_name}://"

    # combine with domain
    # compute final title
    title = get_title(parsed_url)
    post_variants=[title,app_name,domain]
    variants = title_variants_from_domain(domain)
    base_variants = list(set([variant for variant in variants if variant not in post_variants]))
    # update the organized variants
    parsed_url["title_variants"] = get_all_title_variants(variants=base_variants,page=title,name=app_name,domain=domain)

    parsed_url["title"] = pad_or_trim(
        "title",
        string=title,
        title_variants=parsed_url["title_variants"],
        page=title,
        domain=domain,
        name = app_name
    )

    # get keywords
    keywords_info = get_keywords(parsed_url,page=title,domain=domain,name = app_name)
    parsed_url.update(keywords_info)

    keywords = parsed_url.get("keywords", [])

    # FINAL: longest→shortest list with TITLE first, DOMAIN second
    final_variants = [title, parsed_url["domain"]]

    # remove title/domain from pool
    pool = set(keywords + variants)
    pool.discard(title)
    pool.discard(parsed_url["domain"])

    # sort longest → shortest
    final_variants += sort_longest_first(pool)

    parsed_url["title_variants"] = final_variants

    return parsed_url

def get_full_domain(url=None,parsed_url=None):
    parsed_url = parsed_url or get_parsed_url(url)
    http = parsed_url.get("http")
    name = parsed_url.get("name")
    ext = parsed_url.get("ext")
    www = "www." if parsed_url.get("www") else ''
    return f"{http}://{www}{name}{ext}"
def get_full_url(url=None,parsed_url=None):
    parsed_url = parsed_url or get_parsed_url(url)
    full_domain = get_full_domain(url=url,parsed_url=parsed_url)
    path = parsed_url.get("path")
    path = f"/{path}" if path else ''
    return f"{full_domain}{path}"
def get_url_variants(domain,http=None):
    parsed_url = get_parsed_url(domain,http=http)
    stripped_url = parsed_url.copy()
    http = parsed_url.get('http','https') or 'https'
    parsed_url['http']=http
    inverse_http = INVERSE_HTTP.get(http)
    ensured_parsed_url = parsed_url.copy()
    ensured_parsed_url['http'] = http
    
    www = parsed_url.get('www')
    inverse_www = INVERSE_BOOL.get(www)
    parsed_inv_url = ensured_parsed_url.copy()
    parsed_inv_url['www'] = inverse_www
    inverse_parsed_url = ensured_parsed_url.copy()
    inverse_parsed_url['http'] = inverse_http
    inverse_parsed_inv_url = parsed_inv_url.copy()
    inverse_parsed_inv_url['http'] = inverse_http
    url_variants = [ensured_parsed_url,parsed_inv_url,inverse_parsed_url,inverse_parsed_inv_url]
    for i,url_variant in enumerate(url_variants):
        http = url_variant.get("http")
        name = url_variant.get("name")
        ext = url_variant.get("ext")
        path = url_variant.get("path")
        www = "www." if url_variant.get("www") else ''
        path = f"/{path}" if path else ''
        url_variants[i] = f"{http}://{www}{name}{ext}{path}"
    return url_variants
def get_valid_url_variants(domain=None,http=None,variants=None):
    url_variants = variants or get_url_variants(domain=domain,http=http)
    return get_correct_urls(url_variants)
def ensure_http(domain,http=None):
    url_variants = get_url_variants(domain=domain,http=http)
    correct_url = url_variants[0]
    correct_urls = get_correct_urls(url_variants)
    if correct_urls and len(correct_urls) >0:
        correct_url = correct_urls[0]
    return correct_url
