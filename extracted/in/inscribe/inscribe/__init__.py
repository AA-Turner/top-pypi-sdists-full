from ._version import __version__
from inscribe.errors import InscribeAPIException
from requests import HTTPError
import datetime
import base64
import inscribe.config as inscribe_config
import json
import logging
import os
import requests
import urllib
import threading
import atexit

try:
    ENVIRONMENT = os.environ['INSCRIBE_PYTHON_ENV']
except KeyError:
    ENVIRONMENT = 'production'

logger = logging.getLogger("inscribe-api")
config = inscribe_config.config
MS_IN_SECOND = 1000
SECONDS_IN_AN_HOUR = 3600
TIMEOUT_MS = MS_IN_SECOND * SECONDS_IN_AN_HOUR
CHECK_QUEUE_INTERVAL = 10
DEFAULT_API_VERSION = 2
CONFIG = config[ENVIRONMENT]['api']


class Client(object):
    def __init__(self, secret_token: str = None, version: int = None,
                 host: str = CONFIG['url']):
        logger.info("Instantiate API class")

        self._version = version or DEFAULT_API_VERSION
        self.session = requests.Session()
        self.secret_token = secret_token
        self.domain_url = host

        if not self.secret_token:
            raise InscribeAPIException("You must include a secret token. Downgrade to v2.6.0 if you wish to use older forms of Inscribe API keys.")

    def create_customer(self, name: str) -> dict:
        """
        Creates a customer object.

        :param name: A unique name for the customer
        """
        url = "/customers"
        payload = {"name": name}
        return self._post(url, json=payload)

    def get_customer(self, customer_id: str) -> dict:
        """
        Retrieves the details of an existing customer. Supply the unique customer ID from either a
        customer creation request or the customer list, and Inscribe will return the corresponding
        customer information.

        :param id: Unique identifier for the object
        """
        url = f"/customers/{customer_id}"
        return self._get(url)

    def update_customer(self, customer_id: str, name: str, notes: str = None, approved: bool = None) -> dict:
        """
        Updates the specific customer by setting the values of the parameters passed. Any parameters
        not provided will be left unchanged.

        :param customer_id: Unique identifier for the object
        :param name: A unique name for the customer
        :param notes: Any additional notes about this customer that you would like to keep a record of.
        :param approved: Has the value true if you have identified the customer as fraudulent, false is legitimate,
                         and null if unknown. The default is null.
        """
        url = f"/customers/{customer_id}"
        payload = {"name": name}
        if notes is not None:
            payload["notes"] = notes
        if approved is not None:
            payload["approved"] = approved
        return self._put(url, json=payload)

    def delete_customer(self, customer_id: str) -> dict:
        """
        Permanently deletes a customer and all documents associated with this customer. It cannot be undone.
        """
        url = f"/customers/{customer_id}"
        return self._delete(url)


    def get_customers(self, page_number: int = 1, limit_per_page: int = None, search_query: str = None,
         is_approved: bool = None, order_by: str = None, start_date: str = None, end_date: str = None, creator_uuid: str = None, tag = None) -> dict:
        """
        Returns a paginated list of your customers based on optional query parameters. If the customer search query parameter is used,
        the list is sorted by relevance, otherwise the customers are returned sorted by creation date, with the most recently created
        customers appearing first.

        :param page_number: A indicator of which page of the customer list to return (Default: 1)
        :param limit_per_page: A limit on the number of customers to be returned. The limit can range between 1 and 100, and the default is 10.
        :param search_query: A search query for a customer name. Having this query set will override any orderBy by the relevance of the search term.
        :param is_approved: Whether or not the customer has been indicated by you be approved or rejected by you.
        :param order_by: Following options:
                            created_at - customers are returned sorted by ascending creation date
                            -created_at  - customers are returned sorted by descending creation date
        :param start_data and end_date: The date filter allows you to filter customer by date intervals. The value can take any date format supported by the {TODO}.
                             The filter includes everything from the start date up to but not including the end date.
        :param creator_uuid: Returns only customers owned by this user UUID. This user must be in your organization and you must have access to their customers.
        :param tag: Filter customers where at least one document has been marked with the descriptive tag supplied.

        """
        url = f"/customers?page={page_number}"
        if limit_per_page is not None:
            url = url + f"&limit={limit_per_page}"
        if search_query is not None:
            url = url + f"&search={search_query}"
        if is_approved is not None:
            url = url + f"&approved={is_approved}"
        if order_by is not None:
            url = url + f"&order={order_by}"
        if start_date is not None:
            url = url + f"&startDate={start_date}"
        if end_date is not None:
            url = url + f"&endDate={end_date}"
        if creator_uuid is not None:
            url = url + f"&creator={creator_uuid}"
        if tag is not None:
            url = url + f"&tag={tag}"
        return self._get(url)

    def upload_document(self, customer_id: str, document: object, verify_name: str = None, verify_address: str = None, tags: list = list(), verify_id_number: str = None, verify_company: str = None, verify_strings: list = list()):
        """
        Uploads document(s) to a customer. Once the document(s) are uploaded, they will be queued for processing by Inscribe’s fraud detection, parsing,
        and optionally verification algorithms. The file size limit is 50 MB and the page limit for PDFs is 350.

        :param document: The document to be uploaded
        :param verify_name: A name that you want to verify is in a document.
        :param verify_address: An address you want to verify is in a document
        :param tags: A list of descriptive strings chosen by you to group documents together across customers e.g ['onboarding','new_system']
        :param verify_id_number: A id number name that you want to verify is in a document.
        :param verify_company: A company name you want to verify is in a document
        :param verify_strings: A list of dicts with key value pairs for key and input. The key is the identifier for the input and the input is the string you want to verify is in a document e.g [{"key": "phone", input:"929-9774-123"},{"key": "email", input:"john.smith@gmail.com"}]
        """
        url = f"/customers/{customer_id}/documents"
        filename = os.path.basename(document.name)
        verify_entities = []
        if verify_name or verify_address or verify_id_number or verify_company:
            verify_entity = {}
            if verify_name:
                verify_entity["name"] = verify_name
            if verify_address:
                verify_entity["address"] = verify_address
            if verify_id_number:
                verify_entity["id_number"] = verify_id_number
            if verify_company:
                verify_entity["company"] = verify_company
            if verify_strings:
                verify_entity["strings"] = verify_strings
            verify_entities.append(verify_entity)
        formatted_tags = []
        for tag in tags:
            formatted_tags.append({"text": tag})
        files = {
            'verify_entities': (None, json.dumps(verify_entities), 'application/json'),
            'tags': (None, json.dumps(formatted_tags), 'application/json'),
            'file': (filename, document, 'application/octet-stream')
        }
        return self._post(url, files=files)

    def retrieve_document_results(self, customer_id: str, document_id: str, style: str = "compact") -> dict:
        """
        Retrieves the results of an existing document. Supply the unique customer ID from either a customer creation request or the customer list,
        the unique document ID from either a document upload request or document list of the customer, and Inscribe will return the corresponding
        document results if it has finished processing.

        :param customer_id: id of the customer you want to retrieve document results for.
        :param document_id: id of the document you want to retrieve results for.
        """

        url = f"/customers/{customer_id}/documents/{document_id}"
        return self._get(url, params={"style": style})

    def delete_document(self, customer_id: str, document_id: str) -> dict:
        """
        Delete document. This cannot be undone

        :param customer_id: id of customer you want to delete a document from.
        :param document_id: id of document to be deleted.
        """
        url = f"/customers/{customer_id}/documents/{document_id}"
        return self._delete(url)

    def get_all_documents(self, customer_id: str):
        """
        Get all documents for a customer.

        :param customer_id: id of customer you want to get all documents from.
        """
        url = f"/customers/{customer_id}/documents/"
        return self._get(url)

    def add_webhook(self, webhook_url: str):
        """
        Add webhook

        :param webhook_url: the URL that will receive document_processed events.
        """
        url = f"/webhooks/"
        payload = dict(url=webhook_url)
        return self._post(url, payload=payload)

    def get_all_webhooks(self):
        """
        List of all webhooks

        """
        url = f"/webhooks/"
        payload = dict(url=url)
        return self._get(url)

    def get_webhook(self, webhook_id: str):
        """
        List of all webhooks

        :param webhook_id: the ID of the webhook to retrieve.

        """
        url = f"/webhooks/{webhook_id}"
        return self._get(url)

    def delete_webhook(self, webhook_id : str) -> dict:
        """
        Delete webhook. This cannot be undone

        :param webhook_id: id of the webhook to delete.
        """
        url = f"/webhooks/{webhook_id}/"
        return self._delete(url)

    def update_webhook(self, webhook_id : str, webhook_url : str, webhook_type : str) -> dict:
        """
        Update webhook.

        :param webhook_id: id of the webhook to update.
        :param webhook_url: the URL that will receive document_processed events.
        :param webhook_type: the type of the webhook

        """
        url = f"/webhooks/{webhook_id}/"
        payload = dict(url=webhook_url, type=webhook_type)
        return self._put(url, payload=payload)

    @property
    def headers(self):
        return {'Authorization': f"Inscribe {self.secret_token}"}

    @property
    def version(self):
        return "v%s" % self._version

    @property
    def base_url(self):
        return f"{self.domain_url}/api/{self.version}"

    def _get_http_method(self, method_name):
        http_method_mapping = {
            "GET": self.session.get,
            "POST": self.session.post,
            "DELETE": self.session.delete,
            "PUT": self.session.put,
            "PATCH": self.session.patch,
            "HEAD": self.session.head
        }

        try:
            return http_method_mapping[method_name]
        except KeyError:
            raise InscribeAPIException("HTTP method '%s' is invalid!" % method_name)

    def _get(self, url, **kwargs):
        return self._request("GET", url, **kwargs)

    def _post(self, url, **kwargs):
        return self._request("POST", url, **kwargs)

    def _delete(self, url, **kwargs):
        return self._request("DELETE", url, **kwargs)

    def _put(self, url, **kwargs):
        return self._request("PUT", url, **kwargs)

    def _patch(self, url, **kwargs):
        return self._request("PATCH", url, **kwargs)

    def _head(self, url, **kwargs):
        return self._request("HEAD", url, **kwargs)

    def _request(self, method, url, **kwargs):

        http_method = self._get_http_method(method)

        url = self.base_url + url
        logger.info("HTTP %s request. : %s " % (method, url))

        response = http_method(url, headers=self.headers, **kwargs)
        logger.info("Response: %s" % response.text)
        try:
            response.raise_for_status()
        except HTTPError as e:
            logger.info(str(e))
            try:
                response_json = response.json()
            except:
                raise InscribeAPIException(f"{str(e)}\nError occurred during sending a request to {url}")
            raise InscribeAPIException(f"Error occurred during API call: {response_json['message']}")

        try:
            response_json = response.json()
        except:
            if response.status_code == 204:
                return response.text
            raise InscribeAPIException("Couldn't get a valid JSON from response")

        return response_json

    def __del__(self):
        self.session.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
