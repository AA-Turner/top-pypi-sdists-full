from .imports import *

def determine_matching_dict(dict_og,dict_comp):
    
    for key,value in dict_og.items():
        if key not in dict_comp or dict_comp.get(key) != value:
            return False
    return True
def is_header_matching(headers_list,headers_comp):
    headers_list = make_list(headers_list)
    for headers in headers_list:
        if determine_matching_dict(headers,headers_comp):
            return True
    return False
def get_unique_headers_list(existing_headers, new_headers):
    result = list(existing_headers)  # copy
    for candidate in new_headers:
        if not is_header_matching(result, candidate):
            result.append(candidate)
    return result

def get_approved_headers_file_path(directory=None,file_path=None,basename=None):
    basename = basename or 'approved_headers.json'
    if file_path:
        return file_path
    if directory and os.path.isdir(directory):
        file_path = os.path.join(directory,basename)
    else:
        file_path = os.path.join(get_caller_dir(),basename)
    return file_path
def save_approved_headers_dict(data,directory=None,file_path=None,basename=None):
    approved_headers_file_path = get_approved_headers_file_path(directory=directory,file_path=file_path,basename=basename)
    safe_dump_to_json(data=data,file_path=approved_headers_file_path)
def update_approved_headers(obj, url=None, directory=None, file_path=None, basename=None):
    approved_headers_dict = get_approved_headers_dict(
        directory=directory,
        file_path=file_path,
        basename=basename
    )

    if isinstance(obj, list):
        if not url:
            raise ValueError("url is required when obj is a list")
        domain = urlManager(url).parsed.get("domain")
        obj = {domain: obj}

    for domain, values in obj.items():
        current = approved_headers_dict.get(domain, [])
        approved_headers_dict[domain] = get_unique_headers_list(current, values)

    save_approved_headers_dict(
        approved_headers_dict,
        directory=directory,
        file_path=file_path,
        basename=basename
    )
def get_approved_headers_dict(directory=None,file_path=None,basename=None):
    approved_headers_file_path = get_approved_headers_file_path(directory=directory,file_path=file_path,basename=basename)
    if not os.path.isfile(approved_headers_file_path):
        safe_dump_to_json(data={},file_path=approved_headers_file_path)
    return safe_load_from_json(approved_headers_file_path)
def get_approved_headers_for_domain(url):
    domain = urlManager(url).parsed.get("domain")
    approved_headers_dict = get_approved_headers_dict()
    return approved_headers_dict.get(domain, [])
def get_approved_header_for_domain(url,restricted_list=None):
    restricted_list = restricted_list or []
    approved_headers = get_approved_headers_for_domain(url)
    for approved_header in approved_headers:
        if not is_header_matching(approved_header,restricted_list):
            return approved_header
    return derive_approved_headers_for_url(url,return_first_found=True,restricted_list=restricted_list)
def get_check_approved_header(url):
    if not is_header_matching(user_agent_list,headers) and is_header_valid_for_url(url,user_agent,headers):
        user_agent_list.append(headers)
        update_approved_headers(user_agent_list,url=url)
def is_header_valid_for_url(url,user_agent,headers):
    request_mgr = requestManager(url=url,user_agent=user_agent,headers=headers)
    source_code = request_mgr.source_code
    soup = BeautifulSoup(source_code, "html.parser")
    text = soup.text
    if 'review the security of your connection before proceeding' not in text and 'verifying you are human' not in text and 'Please update your browser' not in text and 'Bitte aktualisiere deinen BrowserDein Browser' not in text and 'browser is no longer supported' not in text:
        return True
    return False
def generate_ua_and_headers(url):
    ua_mgr = UserAgentManager(randomAll=True)
    user_agent = ua_mgr.get_user_agent()
    headers = ua_mgr.generate_headers()
    return user_agent,headers 
def derive_approved_headers_for_url(url,return_first_found=False,restricted_list=None):
    restricted_list=restricted_list or []
    user_agent_list = get_approved_headers_for_domain(url)
    while True:
        user_agent,headers = generate_ua_and_headers(url)
        if not is_header_matching(user_agent_list+restricted_list,headers) and is_header_valid_for_url(url,user_agent,headers):
            user_agent_list.append(headers)
            update_approved_headers(user_agent_list,url=url)
            if return_first_found:
                return headers
