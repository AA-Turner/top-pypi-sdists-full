from ..imports import urlparse as _urlparse
from abstract_utilities import SingletonMeta
from .domain_utils import *
from .domain_utils import  get_parsed_url as _get_parsed_url
class DomainManager(metaclass=SingletonMeta):
    def __init__(self,domain=None):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.domains = {}
        if domain:
            check_domains(domain)
    def check_domains(self,url):
        parsed_url = _get_parsed_url(url)
        domain_name = parsed_url.get('name')
        ext = parsed_url.get('ext')
        if not domain_name in self.domains:
            self.domains[domain_name] = {}
        
        path = parsed_url.get('path')
        domain = parsed_url.get('domain')
        http = parsed_url.get('http','https') or 'https'
        parsed_url['http']=http
        if ext not in self.domains[domain_name]:
            self.domains[domain_name][ext] = parsed_url
        if 'paths' not in self.domains[domain_name][ext]:
            self.domains[domain_name][ext]['paths'] = []
            
        if path not in self.domains[domain_name][ext].get('paths',[]):
            self.domains[domain_name][ext]['paths'].append(path)
            del self.domains[domain_name][ext]['path']
        else:
            return self.domains[domain_name][ext]    
        if 'variants' not in self.domains[domain_name][ext]:
            variants = get_url_variants(domain)                        
            self.domains[domain_name][ext]['variants'] = variants
        if 'valid_variants' not in self.domains[domain_name][ext]:
            variants = self.domains[domain_name][ext]['variants']
            valid_url_variants = get_valid_url_variants(domain = domain)
            if valid_url_variants and len(valid_url_variants)>0:
                valid_url_variant = valid_url_variants[0]
                http = get_http(valid_url_variant)
                if http:
                    self.domains[domain_name][ext]['http']=http
            self.domains[domain_name][ext]['valid_variants'] =  valid_url_variants                      
        if 'full_domain' not in self.domains[domain_name][ext]:
            self.domains[domain_name][ext]['full_domain']=ensure_http(domain)
        if 'domain_valid' not in self.domains[domain_name][ext]:
            valid_url_variants = self.domains[domain_name][ext]['valid_variants']
            self.domains[domain_name][ext]['domain_valid']=False if not valid_url_variants else True

        return self.domains[domain_name][ext]
    def get_parsed_url(self,url):
        parsed = self.check_domains(url)
        parsed_url = parsed.copy()
        parsed['path'] = get_domain_path(url)
        return parsed
    def urlparse(self,url):
        parsed = self.check_domains(url)
        full_domain = parsed.get('full_domain')
        parsed['path'] = get_domain_path(url)
        domain = get_full_url(parsed_url=parsed)
        parsed = _urlparse(domain)
        return parsed
domain_mgr = DomainManager()
def get_parsed_url(url):
    parsed_url = domain_mgr.get_parsed_url(url)
    return parsed_url
def urlparse(url):
    parsed_url = domain_mgr.urlparse(url)
    return parsed_url
parse_url = get_parsed_url
