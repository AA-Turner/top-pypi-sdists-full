
from ..urlManager import *
from ..requestManager import *
from ..soupManager import *

class linkManager:
    """
    LinkManager is a class for managing and extracting links and image links from a web page.

    Args:
        url (str): The URL of the web page (default is "https://example.com").
        source_code (str or None): The source code of the web page (default is None).
        url_mgr (UrlManager or None): An instance of UrlManager (default is None).
        request_manager (requestManager or None): An instance of requestManager (default is None).
        soup_manager (SoupManager or None): An instance of SoupManager (default is None).
        image_link_tags (str): HTML tags to identify image links (default is 'img').
        img_link_attrs (str): HTML attributes to identify image link URLs (default is 'src').
        link_tags (str): HTML tags to identify links (default is 'a').
        link_attrs (str): HTML attributes to identify link URLs (default is 'href').
        strict_order_tags (bool): Flag to indicate if tags and attributes should be matched strictly (default is False).
        img_attr_value_desired (list or None): Desired attribute values for image links (default is None).
        img_attr_value_undesired (list or None): Undesired attribute values for image links (default is None).
        link_attr_value_desired (list or None): Desired attribute values for links (default is None).
        link_attr_value_undesired (list or None): Undesired attribute values for links (default is None).
        associated_data_attr (list): HTML attributes to associate with the extracted links (default is ["data-title", 'alt', 'title']).
        get_img (list): HTML attributes used to identify associated images (default is ["data-title", 'alt', 'title']).

    Methods:
        re_initialize(): Reinitialize the LinkManager with the current settings.
        update_url_mgr(url_mgr): Update the URL manager with a new instance.
        update_url(url): Update the URL and reinitialize the LinkManager.
        update_source_code(source_code): Update the source code and reinitialize the LinkManager.
        update_soup_manager(soup_manager): Update the SoupManager and reinitialize the LinkManager.
        update_desired(...): Update the desired settings and reinitialize the LinkManager.
        find_all_desired(...): Find all desired links or image links based on the specified criteria.
        find_all_domain(): Find all unique domain names in the extracted links.

    Note:
        - The LinkManager class helps manage and extract links and image links from web pages.
        - The class provides flexibility in specifying criteria for link extraction.
    """
    def __init__(self,
                 url=None,
                 source_code=None,
                 soup=None,
                 url_mgr=None,
                 req_mgr=None,
                 soup_mgr=None,
                 parse_type=None,
                 image_link_tags='img',
                 img_link_attrs='src',
                 link_tags='a',
                 link_attrs='href',
                 strict_order_tags=False,
                 img_attr_value_desired=None,
                 img_attr_value_undesired=None,
                 link_attr_value_desired=None,
                 link_attr_value_undesired=None,
                 associated_data_attr=["data-title",'alt','title'],
                 get_img=["data-title",'alt','title']
                 ):

        self.url_mgr = get_url_mgr(url=url,url_mgr=url_mgr)
        self.url = get_url(url=url,url_mgr=self.url_mgr)
        self.req_mgr = get_req_mgr(url=self.url,url_mgr=self.url_mgr,source_code=source_code,req_mgr=req_mgr)
        self.source_code = get_source(url=self.url,url_mgr=self.url_mgr,source_code=source_code,req_mgr=self.req_mgr)
        self.soup_mgr = get_soup_mgr(url=self.url,url_mgr=self.url_mgr,source_code=self.source_code,req_mgr=self.req_mgr,soup_mgr=soup_mgr,soup=soup,parse_type=parse_type)
        
        self.soup = get_soup(url=self.url,url_mgr=self.url_mgr,req_mgr=self.req_mgr,source_code=self.source_code,soup_mgr=self.soup_mgr)

        self.strict_order_tags=strict_order_tags
        self.image_link_tags=image_link_tags
        self.img_link_attrs=img_link_attrs
        self.link_tags=link_tags
        self.link_attrs=link_attrs
        self.img_attr_value_desired=img_attr_value_desired
        self.img_attr_value_undesired=img_attr_value_undesired
        self.link_attr_value_desired=link_attr_value_desired
        self.link_attr_value_undesired=link_attr_value_undesired
        self.associated_data_attr=associated_data_attr
        self.get_img=get_img
        self.all_desired_image_links=self.find_all_desired_links(tag=self.image_link_tags,
                                                                 attr=self.img_link_attrs,
                                                                 attr_value_desired=self.img_attr_value_desired,
                                                                 attr_value_undesired=self.img_attr_value_undesired)
        self.all_desired_links=self.find_all_desired_links(tag=self.link_tags,
                                                           attr=self.link_attrs,
                                                           attr_value_desired=self.link_attr_value_desired,
                                                           attr_value_undesired=self.link_attr_value_undesired,
                                                           associated_data_attr=self.associated_data_attr,
                                                           get_img=get_img)

    def re_initialize(self):
        self.all_desired_image_links=self.find_all_desired_links(tag=self.image_link_tags,attr=self.img_link_attrs,strict_order_tags=self.strict_order_tags,attr_value_desired=self.img_attr_value_desired,attr_value_undesired=self.img_attr_value_undesired)
        self.all_desired_links=self.find_all_desired_links(tag=self.link_tags,attr=self.link_attrs,strict_order_tags=self.strict_order_tags,attr_value_desired=self.link_attr_value_desired,attr_value_undesired=self.link_attr_value_undesired,associated_data_attr=self.associated_data_attr,get_img=self.get_img)
    def update_url_mgr(self,url_mgr):
        self.url_mgr=url_mgr
        self.url=self.url_mgr.url
        self.req_mgr.update_url_mgr(url_mgr=self.url_mgr)
        self.soup_mgr.update_url_mgr(url_mgr=self.url_mgr)
        self.source_code=self.soup_mgr.source_code
        self.re_initialize()
    def update_url(self,url):
        self.url=url
        self.url_mgr.update_url(url=self.url)
        self.url=self.url_mgr.url
        self.req_mgr.update_url(url=self.url)
        self.soup_mgr.update_url(url=self.url)
        self.source_code=self.soup_mgr.source_code
        self.re_initialize()
    def update_source_code(self,source_code):
        self.source_code=source_code
        if self.source_code != self.soup_mgr.source_code:
            self.soup_mgr.update_source_code(source_code=self.source_code)
        self.re_initialize()
    def update_soup_manager(self,soup_manager):
        self.soup_mgr=soup_manager
        self.source_code=self.soup_mgr.source_code
        self.re_initialize()
    def update_desired(self,img_attr_value_desired=None,img_attr_value_undesired=None,link_attr_value_desired=None,link_attr_value_undesired=None,image_link_tags=None,img_link_attrs=None,link_tags=None,link_attrs=None,strict_order_tags=None,associated_data_attr=None,get_img=None):
       self.strict_order_tags = strict_order_tags or self.strict_order_tags
       self.img_attr_value_desired=img_attr_value_desired or self.img_attr_value_desired
       self.img_attr_value_undesired=img_attr_value_undesired or self.img_attr_value_undesired
       self.link_attr_value_desired=link_attr_value_desired or self.link_attr_value_desired
       self.link_attr_value_undesired=link_attr_value_undesired or self.link_attr_value_undesired
       self.image_link_tags=image_link_tags or self.image_link_tags
       self.img_link_attrs=img_link_attrs or self.img_link_attrs
       self.link_tags=link_tags or self.link_tags
       self.link_attrs=link_attrs or self.link_attrs
       self.associated_data_attr=associated_data_attr or self.associated_data_attr
       self.get_img=get_img or self.get_img
       self.re_initialize()
    def find_all_desired(self,tag='img',attr='src',strict_order_tags=False,attr_value_desired=None,attr_value_undesired=None,associated_data_attr=None,get_img=None):
        def make_list(obj):
            if isinstance(obj,list) or obj==None:
                return obj
            return [obj]
        def get_desired_value(attr,attr_value_desired=None,attr_value_undesired=None):
            if attr_value_desired:
                for value in attr_value_desired:
                    if value not in attr:
                        return False
            if attr_value_undesired:
                for value in attr_value_undesired:
                    if value in attr:
                        return False
            return True
        attr_value_desired,attr_value_undesired,associated_data_attr,tags,attribs=make_list(attr_value_desired),make_list(attr_value_undesired),make_list(associated_data_attr),make_list(tag),make_list(attr)
        desired_ls = []
        assiciated_data=[]
        for i,tag in enumerate(tags):
            attribs_list=attribs
            if strict_order_tags:
                if len(attribs)<=i:
                    attribs_list=[None]
                else:
                    attribs_list=make_list(attribs[i])
            for attr in attribs_list:
                for component in self.soup_mgr.soup.find_all(tag):
                    if attr in component.attrs and get_desired_value(attr=component[attr],attr_value_desired=attr_value_desired,attr_value_undesired=attr_value_undesired):
                        if component[attr] not in desired_ls:
                            desired_ls.append(component[attr])
                            assiciated_data.append({"value":component[attr]})
                            if associated_data_attr:
                                for data in associated_data_attr:
                                    if data in component.attrs:
                                        assiciated_data[-1][data]=component.attrs[data]
                                        if get_img and component.attrs[data]:
                                            if data in get_img and len(component.attrs[data])!=0:
                                                for each in self.soup_mgr.soup.find_all('img'):
                                                    if 'alt' in each.attrs:
                                                        if each.attrs['alt'] == component.attrs[data] and 'src' in each.attrs:
                                                            assiciated_data[-1]['image']=each.attrs['src']
        desired_ls.append(assiciated_data)
        return desired_ls
    def find_all_domain(self):
        domain = urlparse(self.url_mgr.url).netloc
        domains_ls=[self.url_mgr.url]
        for url in self.all_desired_links[:-1]:
            if self.url_mgr.is_valid_url(url):
                parse = urlparse(url)
                comp_domain = parse.netloc
                if url not in domains_ls and comp_domain == domain:
                    domains_ls.append(url)
        return domains_ls

    def find_all_desired_links(self,tag='img', attr='src',attr_value_desired=None,strict_order_tags=False,attr_value_undesired=None,associated_data_attr=None,all_desired=None,get_img=None):
        all_desired = all_desired or self.find_all_desired(tag=tag,attr=attr,strict_order_tags=strict_order_tags,attr_value_desired=attr_value_desired,attr_value_undesired=attr_value_undesired,associated_data_attr=associated_data_attr,get_img=get_img)
        assiciated_attrs = all_desired[-1]
        valid_assiciated_attrs = []
        desired_links=[]
        for i,attr in enumerate(all_desired[:-1]):

            self.url_mgr.domain = self.url_mgr.domain or ''

            self.url_mgr.protocol = self.url_mgr.protocol or 'https'
 
            if attr:
                valid_attr=self.url_mgr.make_valid(attr,self.url_mgr.protocol+'://'+self.url_mgr.domain) 
                if valid_attr:
                    desired_links.append(valid_attr)
                    valid_assiciated_attrs.append(assiciated_attrs[i])
                    valid_assiciated_attrs[-1]["link"]=valid_attr
        desired_links.append(valid_assiciated_attrs)
        return desired_links

    
