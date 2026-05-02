from ._decorators import deprecated
from . import _VDAPIService, _VDAPIResponse, _VDAPISingleResponse

class _BulkListResponse(_VDAPISingleResponse):

    __LIST_API__ = ""
    __LIST_PAYLOAD_ENTRY__=""

    def _to_list(self, input_list):
        """
        The api needs a list, and you can't serialize sets, or Series
        """
        if isinstance(input_list, list):
            return input_list

        return [x for x in input_list]

    def get_list(self, **kwargs): 
        return self._service.get("{}/{}".format(self.id, self.__LIST_API__), **kwargs)

    def _bulk_path(self, param):
        return "{}/{}/{}".format(self.id, self.__LIST_API__, param)

    def _bulk_post(self, input_list, path, file_path=None):
        
        files = None
        if file_path:
            files={'csv_file': ('csv_file', open(file_path, 'rb'), "multipart/form-data") }
            path = "file_{}".format(path)

        payload = {self.__LIST_PAYLOAD_ENTRY__:self._to_list(input_list)}
        resp = self._service.post(payload, path_param=self._bulk_path(path),
                                  files=files)
        return resp

    def bulk_create(self, input_list=[], file_path=None): 
        """
        Appends this list to the existing list

            input_list: List of items to upload. Max 100k at a time
            file_path: file path to a csv of items.  This can be much larger (in the millions)
        """
        return self._bulk_post(input_list, 'bulk_create', file_path=file_path)

    def bulk_replace(self, input_list=[], file_path=None):
        """
        Replaces the existing list with this list

            input_list: List of items to upload. Max 100k at a time
            file_path: file path to a csv of items.  This can be much larger (in the millions)
        """
        return self._bulk_post(input_list, 'bulk_replace', file_path=file_path)

    def bulk_delete(self, input_list=[], file_path=None):
        """
        removes these items from the existing list
        """
        path = 'bulk_delete'
        files = None
        if file_path:
            files={'csv_file': ('csv_file', open(file_path, 'rb'),
                                "multipart/form-data")}
            path = "file_{}".format(path)

        payload = {self.__LIST_PAYLOAD_ENTRY__:self._to_list(input_list)}
        return self._service.bulk_delete(payload,
                                         path_param=self._bulk_path(path),
                                         files=files)


class _AdvertiserDomainListResponse(_BulkListResponse):
    """
    Override to give you access to the actual domains
    """
    __LIST_API__ = "advertiser_domains"
    __LIST_PAYLOAD_ENTRY__="names"

    @deprecated("use get_list() instead")
    def get_domains(self, **kwargs):
        """
        Get the list of domains that are in this domain list

            d = springserve.domain_list.get(id)
            domains = d.get_domains()

            for domain in domains:
                print domain.name

        """
        return self.get_list(**kwargs)
    
    @deprecated("use bulk_create() instead")
    def add_domains(self, domains):
        """
        Add a list of domains to this domain list

            d = springserve.domain_list.get(id)
            d.add_domains(['blah.com', 'blah2.com'])

        domains: List of domains you would like to add 
        """
        return self.bulk_create(domains)

    @deprecated("use bulk_delete() instead")
    def remove_domains(self, domains):
        """
        Add a list of domains to this domain list

            d = springserve.domain_list.get(id)
            d.remove_domains(['blah.com', 'blah2.com'])

        domains: List of domains you would like to add 
        """
        return self.bulk_delete(domains)


class _AdvertiserDomainListAPI(_VDAPIService):

    __API__ = "advertiser_domain_lists"
    __RESPONSE_OBJECT__ = _AdvertiserDomainListResponse


class _DomainListResponse(_BulkListResponse):
    """
    Override to give you access to the actual domains
    """
    __LIST_API__ = "domains"
    __LIST_PAYLOAD_ENTRY__="names"

    @deprecated("use get_list() instead")
    def get_domains(self, **kwargs):
        """
        Get the list of domains that are in this domain list

            d = springserve.domain_list.get(id)
            domains = d.get_domains()

            for domain in domains:
                print domain.name

        """
        return self.get_list(**kwargs)
    
    @deprecated("use bulk_create() instead")
    def add_domains(self, domains):
        """
        Add a list of domains to this domain list

            d = springserve.domain_list.get(id)
            d.add_domains(['blah.com', 'blah2.com'])

        domains: List of domains you would like to add 
        """
        return self.bulk_create(domains)

    @deprecated("use bulk_delete() instead")
    def remove_domains(self, domains):
        """
        Add a list of domains to this domain list

            d = springserve.domain_list.get(id)
            d.remove_domains(['blah.com', 'blah2.com'])

        domains: List of domains you would like to add 
        """
        return self.bulk_delete(domains)


class _DomainListAPI(_VDAPIService):

    __API__ = "domain_lists"
    __RESPONSE_OBJECT__ = _DomainListResponse



class _AppBundleListResponse(_BulkListResponse):
    """
    Override to give you access to the actual domains
    """
    __LIST_API__ = "app_bundles"
    __LIST_PAYLOAD_ENTRY__="app_bundles"

    @deprecated("use get_list() instead")
    def get_bundles(self, **kwargs):
        """
        Get the list of domains that are in this domain list

            d = springserve.domain_list.get(id)
            domains = d.get_domains()

            for domain in domains:
                print domain.name

        """
        return self.get_list(**kwargs)
    
    @deprecated("use bulk_create() instead")
    def add_bundles(self, bundles):
        """
        Add a list of domains to this domain list

            d = springserve.domain_list.get(id)
            d.add_domains(['blah.com', 'blah2.com'])

        domains: List of domains you would like to add 
        """
        return self.bulk_create(bundles)

    @deprecated("use bulk_delete() instead")
    def remove_bundles(self, bundles):
        """
        Add a list of domains to this domain list

            d = springserve.domain_list.get(id)
            d.remove_domains(['blah.com', 'blah2.com'])

        domains: List of domains you would like to add 
        """
        return self.bulk_delete(bundles)


class _AppBundleListAPI(_VDAPIService):

    __API__ = "app_bundle_lists"
    __RESPONSE_OBJECT__ = _AppBundleListResponse

class _AppNameListResponse(_BulkListResponse):
    """
    Override to give you access to the actual domains
    """

    __LIST_API__ = "app_names"
    __LIST_PAYLOAD_ENTRY__="app_names"

    @deprecated("use get_list() instead")
    def get_names(self, **kwargs):
        """
        Get the list of domains that are in this domain list

            d = springserve.domain_list.get(id)
            domains = d.get_domains()

            for domain in domains:
                print domain.name

        """
        return self.get_list(**kwargs)
    
    @deprecated("use bulk_create() instead")
    def add_names(self, names):
        """
        Add a list of domains to this domain list

            d = springserve.domain_list.get(id)
            d.add_domains(['blah.com', 'blah2.com'])

        domains: List of domains you would like to add 
        """
        return self.bulk_create(names)

    @deprecated("use bulk_delete() instead")
    def remove_names(self, names):
        """
        Add a list of domains to this domain list

            d = springserve.domain_list.get(id)
            d.remove_domains(['blah.com', 'blah2.com'])

        domains: List of domains you would like to add 
        """
        return self.bulk_delete(names)


class _AppNameListAPI(_VDAPIService):

    __API__ = "app_name_lists"
    __RESPONSE_OBJECT__ = _AppNameListResponse


class _SegmentListResponse(_BulkListResponse):
    """
    Override to give you access to the actual device ids
    """
    __LIST_API__ = "items"
    __LIST_PAYLOAD_ENTRY__="items"

class _SegmentListAPI(_VDAPIService):

    __API__ = "segments"
    __RESPONSE_OBJECT__ = _SegmentListResponse

class _ChannelIdListResponse(_BulkListResponse):

    __LIST_API__ = "channel_ids"
    __LIST_PAYLOAD_ENTRY__="channel_ids"

class _ChannelIdListAPI(_VDAPIService):

    __API__ = "channel_id_lists"
    __RESPONSE_OBJECT__ = _ChannelIdListResponse

class _DealIdListResponse(_BulkListResponse):

    __LIST_API__ = "deal_ids"
    __LIST_PAYLOAD_ENTRY__="deal_ids"

class _DealIdListAPI(_VDAPIService):

    __API__ = "deal_id_lists"
    __RESPONSE_OBJECT__ = _DealIdListResponse

class _PlacementIdListResponse(_BulkListResponse):

    __LIST_API__ = "placement_ids"
    __LIST_PAYLOAD_ENTRY__="placement_ids"

class _PlacementIdListAPI(_VDAPIService):

    __API__ =  "placement_id_lists"
    __RESPONSE_OBJECT__ = _PlacementIdListResponse

class _ParameterListResponse(_BulkListResponse):

    __LIST_API__ = "values"
    __LIST_PAYLOAD_ENTRY__="values"

class _ParameterListAPI(_VDAPIService):

    __API__ =  "parameter_lists"
    __RESPONSE_OBJECT__ = _ParameterListResponse

class _PublisherIdListResponse(_BulkListResponse):

    __LIST_API__ = "publisher_ids"
    __LIST_PAYLOAD_ENTRY__="publisher_ids"

class _PublisherIdListAPI(_VDAPIService):

    __API__ = "publisher_id_lists"
    __RESPONSE_OBJECT__ = _PublisherIdListResponse

class _IpListResponse(_BulkListResponse):
    """
    Override to give you access to the actual ips
    """
    __LIST_API__ = "ips"
    __LIST_PAYLOAD_ENTRY__="ips"

    @deprecated("use get_list() instead")
    def get_ips(self, **kwargs):
        """
        Get the list of ips that are in this ip list

            d = springserve.ip_lists.get(id)
            ips = d.get_ips()

            for i in ips:
                print i.ip

        """
        return self.get_list(**kwargs)

    @deprecated("use bulk_create() instead")
    def add_ips(self, ips):
        """
        Add a list of ips to this ip list

            d = springserve.ip_lists.get(id)
            d.add_ips(['123', '124'])

        ips: List of ips you would like to add
        """
        return self.bulk_create(ips)

    @deprecated("use bulk_delete() instead")
    def remove_ips(self, ips):
        """
        Remove a list of ips from this ip list

            d = springserve.ip_lists.get(id)
            d.remove_ips(['123', '124'])

        ips: List of ips you would like to remove
        """
        return self.bulk_delete(ips)


class _IpListAPI(_VDAPIService):

    __API__ = "ip_lists"
    __RESPONSE_OBJECT__ = _IpListResponse


class _BillItemAPI(_VDAPIService):

    __API__ = "bill_items"

    def __init__(self, bill_id):
        super(_BillItemAPI, self).__init__()
        self.bill_id = bill_id

    @property
    def endpoint(self):
        """
        The api endpoint that is used for this service.  For example:: 
            
            In [1]: import springserve

            In [2]: springserve.supply_tags.endpoint
            Out[2]: '/supply_tags'

        """
        return "/bills/{}/bill_items".format(self.bill_id)


class _BillResponse(_VDAPISingleResponse):
    
    def get_bill_items(self):
        # Need to make a new one per bill
        return _BillItemAPI(self.id).get()

    def _add_bill_item(self, data, **kwargs):
        return _BillItemAPI(self.id).post(data, **kwargs)


class _BillAPI(_VDAPIService):

    __API__ = "bills"
    __RESPONSE_OBJECT__ = _BillResponse

    def bulk_sync(self, ids, reauth=False, **query_params):
        query_params['ids'] = ','.join(str(x) for x in ids)

        return self.get('bulk_sync', reauth, **query_params)

class _ValueAPI(_VDAPIService):

    __API__ = "values"

    def __init__(self, key):
        super(_ValueAPI, self).__init__()
        self.key_id = key.id
        self.account_id = key.account_id 

    @property
    def endpoint(self):
       return "/keys/{}/values".format(self.key_id)


class _KeyResponse(_VDAPISingleResponse):

    def get_values(self):
        return _ValueAPI(self).get()

    def add_value(self, data, **kwargs):
        return _ValueAPI(self).post(data, **kwargs)
 
class _KeyAPI(_VDAPIService):

    __API__ = "keys"
    __RESPONSE_OBJECT__ = _KeyResponse

