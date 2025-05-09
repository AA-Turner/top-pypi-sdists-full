# coding: utf-8

"""
    PowerBot - Webservice for algotrading

    # TERMS AND CONDITIONS The PowerBot system provides B2B services for trading at intraday power markets. By using the PowerBot service, each user agrees to the terms and conditions of this licence: 1. The user confirms that they are familiar with the exchanges trading system and all relevant rules, is professionally qualified and in possession of a trading license for the relevant exchange. 2. The user will comply with the exchanges market rules (e.g. [EPEX Spot Market Rules](https://www.epexspot.com/en/downloads#rules-fees-processes) or [Nord Pool Market Rules](https://www.nordpoolgroup.com/trading/Rules-and-regulations/)) and will not endanger the exchange system at any time with heavy load from trading algorithms or by other use. 3. The user is aware of limits imposed by the exchange. 4. The user is solely liable for actions resulting from the use of PowerBot.   # INTRODUCTION PowerBot is a web-based software service enabling algorithmic trading on intraday power exchanges such as EPEX, Nord Pool, HUPX, BSP Southpool, TGE, OPCOM or ETPA. The service is straightforward to integrate in an existing software environment and provides a variety of programming interfaces for development of individual trading algorithms and software tools. Besides enabling fully automated intraday trading, it can be used to create tools for human traders providing relevant information and trading opportunities or can be integrated in existing software tools. For further details see https://www.powerbot-trading.com  ## Knowledge Base In addition to this API guide, please find the documentation at https://docs.powerbot-trading.com - the password will be provided by the PowerBot team. If not, please reach out to us at support@powerbot-trading.com  ## Endpoints The PowerBot service is available at the following REST endpoints:  | Instance      | Base URL for REST Endpoints                                      | |---------------|------------------------------------------------------------------| | EPEX          | https://staging.powerbot-trading.com/playground/epex/v2/api      | | Nord Pool     | https://staging.powerbot-trading.com/playground/nordpool/v2/api  | | HUPX          | https://staging.powerbot-trading.com/playground/hupx/v2/api      | | BSP Southpool | https://staging.powerbot-trading.com/playground/southpool/v2/api | | TGE           | https://staging.powerbot-trading.com/playground/tge/v2/api       | | IBEX          | https://staging.powerbot-trading.com/playground/ibex/v2/api      | | CROPEX        | https://staging.powerbot-trading.com/playground/cropex/v2/api    | | OPCOM         | https://staging.powerbot-trading.com/playground/opcom/v2/api     | | ETPA          | https://staging.powerbot-trading.com/playground/etpa/v2/api      | | BRM           | https://staging.powerbot-trading.com/playground/brm/v2/api       |  Access to endpoints is secured via an API Key, which needs to be passed as an \"api_key\" header in each request.   Notes on API Keys:  * API keys are specific to Test, Staging or Production.  * API keys are generated by the system administrator and need to be requested.  ## How to generate API clients (libraries) This OpenAPI specification can be used to generate API clients (programming libraries) for a wide range of programming languages using tools like [OpenAPI Generator](https://openapi-generator.tech/). A detailed guide can be found in the [knowledge base](https://docs.powerbot-trading.com/articles/getting-started/generating-clients/).  ## PowerBot Python client For Python, a ready-made client is also available on PyPI and can be downloaded locally via:  ```shell   pip install powerbot-client ```  ## Errors The API uses standard HTTP status codes to indicate the success or failure of the API call. The body of the response will be in JSON format as follows:  ``` {   \"message\": \"... an error message ...\" } ```  ## Paging The API uses offset and limit parameters for paged operations. An X-Total-Count header is added to responses to indicate the total number of items in a paged response.  ## API Rate Limiting The API limits the number of concurrent calls to 50 - when that limit is reached, the client will receive 503 http status codes (service unavailable) with the following text:  ``` {   \"message\": \"API rate limit exceeded\" } ``` Clients should ensure that they stay within the limit for concurrent API calls.    ## Additional code samples Additional information and code samples demonstrating the use of the API can be found at in our [knowledge base](https://docs.powerbot-trading.com/docs/programmatic-access/)  # noqa: E501

    The version of the OpenAPI document: 2.22.1
    Contact: office@powerbot-trading.com
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from powerbot_client.configuration import Configuration


class MarketStatus(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'server_version': 'str',
        'exchange': 'Exchange',
        'exchange_mode': 'str',
        'exchange_user': 'str',
        'app_id': 'str',
        'api_timestamp': 'datetime',
        'certificate_expiration_date': 'datetime',
        'status': 'MarketState',
        'options': 'MarketOptions',
        'atc_status': 'AtcStatus',
        'urls': 'list[str]',
        'products': 'list[str]',
        'market_area_id': 'str',
        'delivery_area_id': 'str',
        'available_delivery_area_ids': 'list[str]',
        'inactive_delivery_area_ids': 'list[str]',
        'exchange_limits': 'list[ExchangeCashLimit]',
        'session_id': 'str',
        'logged_in_since': 'datetime',
        'heartbeat_as_of': 'datetime',
        'heartbeat_content': 'str',
        'mfa_supported': 'bool',
        'mfa_secret': 'str',
        'messages': 'list[str]',
        'mode': 'str',
        'order_action_quota': 'float',
        'available_account_ids': 'list[str]',
        'session_max_age': 'int',
        'session_max_inactive_time': 'int'
    }

    attribute_map = {
        'server_version': 'server_version',
        'exchange': 'exchange',
        'exchange_mode': 'exchange_mode',
        'exchange_user': 'exchange_user',
        'app_id': 'app_id',
        'api_timestamp': 'api_timestamp',
        'certificate_expiration_date': 'certificate_expiration_date',
        'status': 'status',
        'options': 'options',
        'atc_status': 'atc_status',
        'urls': 'urls',
        'products': 'products',
        'market_area_id': 'market_area_id',
        'delivery_area_id': 'delivery_area_id',
        'available_delivery_area_ids': 'available_delivery_area_ids',
        'inactive_delivery_area_ids': 'inactive_delivery_area_ids',
        'exchange_limits': 'exchange_limits',
        'session_id': 'session_id',
        'logged_in_since': 'logged_in_since',
        'heartbeat_as_of': 'heartbeat_as_of',
        'heartbeat_content': 'heartbeat_content',
        'mfa_supported': 'mfa_supported',
        'mfa_secret': 'mfa_secret',
        'messages': 'messages',
        'mode': 'mode',
        'order_action_quota': 'order_action_quota',
        'available_account_ids': 'available_account_ids',
        'session_max_age': 'session_max_age',
        'session_max_inactive_time': 'session_max_inactive_time'
    }

    def __init__(self, server_version=None, exchange=None, exchange_mode=None, exchange_user=None, app_id=None, api_timestamp=None, certificate_expiration_date=None, status=None, options=None, atc_status=None, urls=None, products=None, market_area_id=None, delivery_area_id=None, available_delivery_area_ids=None, inactive_delivery_area_ids=None, exchange_limits=None, session_id=None, logged_in_since=None, heartbeat_as_of=None, heartbeat_content=None, mfa_supported=None, mfa_secret=None, messages=None, mode=None, order_action_quota=None, available_account_ids=None, session_max_age=None, session_max_inactive_time=None, local_vars_configuration=None):  # noqa: E501
        """MarketStatus - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._server_version = None
        self._exchange = None
        self._exchange_mode = None
        self._exchange_user = None
        self._app_id = None
        self._api_timestamp = None
        self._certificate_expiration_date = None
        self._status = None
        self._options = None
        self._atc_status = None
        self._urls = None
        self._products = None
        self._market_area_id = None
        self._delivery_area_id = None
        self._available_delivery_area_ids = None
        self._inactive_delivery_area_ids = None
        self._exchange_limits = None
        self._session_id = None
        self._logged_in_since = None
        self._heartbeat_as_of = None
        self._heartbeat_content = None
        self._mfa_supported = None
        self._mfa_secret = None
        self._messages = None
        self._mode = None
        self._order_action_quota = None
        self._available_account_ids = None
        self._session_max_age = None
        self._session_max_inactive_time = None
        self.discriminator = None

        if server_version is not None:
            self.server_version = server_version
        if exchange is not None:
            self.exchange = exchange
        if exchange_mode is not None:
            self.exchange_mode = exchange_mode
        if exchange_user is not None:
            self.exchange_user = exchange_user
        if app_id is not None:
            self.app_id = app_id
        if api_timestamp is not None:
            self.api_timestamp = api_timestamp
        if certificate_expiration_date is not None:
            self.certificate_expiration_date = certificate_expiration_date
        self.status = status
        if options is not None:
            self.options = options
        if atc_status is not None:
            self.atc_status = atc_status
        if urls is not None:
            self.urls = urls
        if products is not None:
            self.products = products
        if market_area_id is not None:
            self.market_area_id = market_area_id
        if delivery_area_id is not None:
            self.delivery_area_id = delivery_area_id
        if available_delivery_area_ids is not None:
            self.available_delivery_area_ids = available_delivery_area_ids
        if inactive_delivery_area_ids is not None:
            self.inactive_delivery_area_ids = inactive_delivery_area_ids
        if exchange_limits is not None:
            self.exchange_limits = exchange_limits
        if session_id is not None:
            self.session_id = session_id
        if logged_in_since is not None:
            self.logged_in_since = logged_in_since
        if heartbeat_as_of is not None:
            self.heartbeat_as_of = heartbeat_as_of
        if heartbeat_content is not None:
            self.heartbeat_content = heartbeat_content
        if mfa_supported is not None:
            self.mfa_supported = mfa_supported
        if mfa_secret is not None:
            self.mfa_secret = mfa_secret
        if messages is not None:
            self.messages = messages
        if mode is not None:
            self.mode = mode
        if order_action_quota is not None:
            self.order_action_quota = order_action_quota
        if available_account_ids is not None:
            self.available_account_ids = available_account_ids
        if session_max_age is not None:
            self.session_max_age = session_max_age
        if session_max_inactive_time is not None:
            self.session_max_inactive_time = session_max_inactive_time

    @property
    def server_version(self):
        """Gets the server_version of this MarketStatus.  # noqa: E501


        :return: The server_version of this MarketStatus.  # noqa: E501
        :rtype: str
        """
        return self._server_version

    @server_version.setter
    def server_version(self, server_version):
        """Sets the server_version of this MarketStatus.


        :param server_version: The server_version of this MarketStatus.  # noqa: E501
        :type server_version: str
        """

        self._server_version = server_version

    @property
    def exchange(self):
        """Gets the exchange of this MarketStatus.  # noqa: E501


        :return: The exchange of this MarketStatus.  # noqa: E501
        :rtype: Exchange
        """
        return self._exchange

    @exchange.setter
    def exchange(self, exchange):
        """Sets the exchange of this MarketStatus.


        :param exchange: The exchange of this MarketStatus.  # noqa: E501
        :type exchange: Exchange
        """

        self._exchange = exchange

    @property
    def exchange_mode(self):
        """Gets the exchange_mode of this MarketStatus.  # noqa: E501


        :return: The exchange_mode of this MarketStatus.  # noqa: E501
        :rtype: str
        """
        return self._exchange_mode

    @exchange_mode.setter
    def exchange_mode(self, exchange_mode):
        """Sets the exchange_mode of this MarketStatus.


        :param exchange_mode: The exchange_mode of this MarketStatus.  # noqa: E501
        :type exchange_mode: str
        """
        allowed_values = ["production", "simulation"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and exchange_mode not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `exchange_mode` ({0}), must be one of {1}"  # noqa: E501
                .format(exchange_mode, allowed_values)
            )

        self._exchange_mode = exchange_mode

    @property
    def exchange_user(self):
        """Gets the exchange_user of this MarketStatus.  # noqa: E501

        The user that is use to authenticate with the exchange  # noqa: E501

        :return: The exchange_user of this MarketStatus.  # noqa: E501
        :rtype: str
        """
        return self._exchange_user

    @exchange_user.setter
    def exchange_user(self, exchange_user):
        """Sets the exchange_user of this MarketStatus.

        The user that is use to authenticate with the exchange  # noqa: E501

        :param exchange_user: The exchange_user of this MarketStatus.  # noqa: E501
        :type exchange_user: str
        """

        self._exchange_user = exchange_user

    @property
    def app_id(self):
        """Gets the app_id of this MarketStatus.  # noqa: E501


        :return: The app_id of this MarketStatus.  # noqa: E501
        :rtype: str
        """
        return self._app_id

    @app_id.setter
    def app_id(self, app_id):
        """Sets the app_id of this MarketStatus.


        :param app_id: The app_id of this MarketStatus.  # noqa: E501
        :type app_id: str
        """

        self._app_id = app_id

    @property
    def api_timestamp(self):
        """Gets the api_timestamp of this MarketStatus.  # noqa: E501

        The timestamp when the status of the market was last checked.  # noqa: E501

        :return: The api_timestamp of this MarketStatus.  # noqa: E501
        :rtype: datetime
        """
        return self._api_timestamp

    @api_timestamp.setter
    def api_timestamp(self, api_timestamp):
        """Sets the api_timestamp of this MarketStatus.

        The timestamp when the status of the market was last checked.  # noqa: E501

        :param api_timestamp: The api_timestamp of this MarketStatus.  # noqa: E501
        :type api_timestamp: datetime
        """

        self._api_timestamp = api_timestamp

    @property
    def certificate_expiration_date(self):
        """Gets the certificate_expiration_date of this MarketStatus.  # noqa: E501

        The expiration date of the client certificate  # noqa: E501

        :return: The certificate_expiration_date of this MarketStatus.  # noqa: E501
        :rtype: datetime
        """
        return self._certificate_expiration_date

    @certificate_expiration_date.setter
    def certificate_expiration_date(self, certificate_expiration_date):
        """Sets the certificate_expiration_date of this MarketStatus.

        The expiration date of the client certificate  # noqa: E501

        :param certificate_expiration_date: The certificate_expiration_date of this MarketStatus.  # noqa: E501
        :type certificate_expiration_date: datetime
        """

        self._certificate_expiration_date = certificate_expiration_date

    @property
    def status(self):
        """Gets the status of this MarketStatus.  # noqa: E501


        :return: The status of this MarketStatus.  # noqa: E501
        :rtype: MarketState
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this MarketStatus.


        :param status: The status of this MarketStatus.  # noqa: E501
        :type status: MarketState
        """
        if self.local_vars_configuration.client_side_validation and status is None:  # noqa: E501
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

    @property
    def options(self):
        """Gets the options of this MarketStatus.  # noqa: E501


        :return: The options of this MarketStatus.  # noqa: E501
        :rtype: MarketOptions
        """
        return self._options

    @options.setter
    def options(self, options):
        """Sets the options of this MarketStatus.


        :param options: The options of this MarketStatus.  # noqa: E501
        :type options: MarketOptions
        """

        self._options = options

    @property
    def atc_status(self):
        """Gets the atc_status of this MarketStatus.  # noqa: E501


        :return: The atc_status of this MarketStatus.  # noqa: E501
        :rtype: AtcStatus
        """
        return self._atc_status

    @atc_status.setter
    def atc_status(self, atc_status):
        """Sets the atc_status of this MarketStatus.


        :param atc_status: The atc_status of this MarketStatus.  # noqa: E501
        :type atc_status: AtcStatus
        """

        self._atc_status = atc_status

    @property
    def urls(self):
        """Gets the urls of this MarketStatus.  # noqa: E501

        The urls of the exchange's backend system the server is connected to  # noqa: E501

        :return: The urls of this MarketStatus.  # noqa: E501
        :rtype: list[str]
        """
        return self._urls

    @urls.setter
    def urls(self, urls):
        """Sets the urls of this MarketStatus.

        The urls of the exchange's backend system the server is connected to  # noqa: E501

        :param urls: The urls of this MarketStatus.  # noqa: E501
        :type urls: list[str]
        """

        self._urls = urls

    @property
    def products(self):
        """Gets the products of this MarketStatus.  # noqa: E501

        DEPRECATED: Use `GET /delivery-areas` or `GET /delivery-area/{area_id}` instead. Exchange's products which the server is linked with  # noqa: E501

        :return: The products of this MarketStatus.  # noqa: E501
        :rtype: list[str]
        """
        return self._products

    @products.setter
    def products(self, products):
        """Sets the products of this MarketStatus.

        DEPRECATED: Use `GET /delivery-areas` or `GET /delivery-area/{area_id}` instead. Exchange's products which the server is linked with  # noqa: E501

        :param products: The products of this MarketStatus.  # noqa: E501
        :type products: list[str]
        """

        self._products = products

    @property
    def market_area_id(self):
        """Gets the market_area_id of this MarketStatus.  # noqa: E501

        The markets the server is configured to operate in  # noqa: E501

        :return: The market_area_id of this MarketStatus.  # noqa: E501
        :rtype: str
        """
        return self._market_area_id

    @market_area_id.setter
    def market_area_id(self, market_area_id):
        """Sets the market_area_id of this MarketStatus.

        The markets the server is configured to operate in  # noqa: E501

        :param market_area_id: The market_area_id of this MarketStatus.  # noqa: E501
        :type market_area_id: str
        """

        self._market_area_id = market_area_id

    @property
    def delivery_area_id(self):
        """Gets the delivery_area_id of this MarketStatus.  # noqa: E501

        The default delivery area (EIC) the server is configured to operate in  # noqa: E501

        :return: The delivery_area_id of this MarketStatus.  # noqa: E501
        :rtype: str
        """
        return self._delivery_area_id

    @delivery_area_id.setter
    def delivery_area_id(self, delivery_area_id):
        """Sets the delivery_area_id of this MarketStatus.

        The default delivery area (EIC) the server is configured to operate in  # noqa: E501

        :param delivery_area_id: The delivery_area_id of this MarketStatus.  # noqa: E501
        :type delivery_area_id: str
        """

        self._delivery_area_id = delivery_area_id

    @property
    def available_delivery_area_ids(self):
        """Gets the available_delivery_area_ids of this MarketStatus.  # noqa: E501

        The available delivery areas EICs  # noqa: E501

        :return: The available_delivery_area_ids of this MarketStatus.  # noqa: E501
        :rtype: list[str]
        """
        return self._available_delivery_area_ids

    @available_delivery_area_ids.setter
    def available_delivery_area_ids(self, available_delivery_area_ids):
        """Sets the available_delivery_area_ids of this MarketStatus.

        The available delivery areas EICs  # noqa: E501

        :param available_delivery_area_ids: The available_delivery_area_ids of this MarketStatus.  # noqa: E501
        :type available_delivery_area_ids: list[str]
        """

        self._available_delivery_area_ids = available_delivery_area_ids

    @property
    def inactive_delivery_area_ids(self):
        """Gets the inactive_delivery_area_ids of this MarketStatus.  # noqa: E501

        Delivery areas that are accessible through the exchange API, but not unlocked in PowerBot.  # noqa: E501

        :return: The inactive_delivery_area_ids of this MarketStatus.  # noqa: E501
        :rtype: list[str]
        """
        return self._inactive_delivery_area_ids

    @inactive_delivery_area_ids.setter
    def inactive_delivery_area_ids(self, inactive_delivery_area_ids):
        """Sets the inactive_delivery_area_ids of this MarketStatus.

        Delivery areas that are accessible through the exchange API, but not unlocked in PowerBot.  # noqa: E501

        :param inactive_delivery_area_ids: The inactive_delivery_area_ids of this MarketStatus.  # noqa: E501
        :type inactive_delivery_area_ids: list[str]
        """

        self._inactive_delivery_area_ids = inactive_delivery_area_ids

    @property
    def exchange_limits(self):
        """Gets the exchange_limits of this MarketStatus.  # noqa: E501


        :return: The exchange_limits of this MarketStatus.  # noqa: E501
        :rtype: list[ExchangeCashLimit]
        """
        return self._exchange_limits

    @exchange_limits.setter
    def exchange_limits(self, exchange_limits):
        """Sets the exchange_limits of this MarketStatus.


        :param exchange_limits: The exchange_limits of this MarketStatus.  # noqa: E501
        :type exchange_limits: list[ExchangeCashLimit]
        """

        self._exchange_limits = exchange_limits

    @property
    def session_id(self):
        """Gets the session_id of this MarketStatus.  # noqa: E501

        The current session id with the exchange  # noqa: E501

        :return: The session_id of this MarketStatus.  # noqa: E501
        :rtype: str
        """
        return self._session_id

    @session_id.setter
    def session_id(self, session_id):
        """Sets the session_id of this MarketStatus.

        The current session id with the exchange  # noqa: E501

        :param session_id: The session_id of this MarketStatus.  # noqa: E501
        :type session_id: str
        """

        self._session_id = session_id

    @property
    def logged_in_since(self):
        """Gets the logged_in_since of this MarketStatus.  # noqa: E501

        The timestamp (UTC) of the start of the current connection to the exchange.  # noqa: E501

        :return: The logged_in_since of this MarketStatus.  # noqa: E501
        :rtype: datetime
        """
        return self._logged_in_since

    @logged_in_since.setter
    def logged_in_since(self, logged_in_since):
        """Sets the logged_in_since of this MarketStatus.

        The timestamp (UTC) of the start of the current connection to the exchange.  # noqa: E501

        :param logged_in_since: The logged_in_since of this MarketStatus.  # noqa: E501
        :type logged_in_since: datetime
        """

        self._logged_in_since = logged_in_since

    @property
    def heartbeat_as_of(self):
        """Gets the heartbeat_as_of of this MarketStatus.  # noqa: E501

        The timestamp when the last heartbeat of the backend system has been received (should be not older than 5 seconds)  # noqa: E501

        :return: The heartbeat_as_of of this MarketStatus.  # noqa: E501
        :rtype: datetime
        """
        return self._heartbeat_as_of

    @heartbeat_as_of.setter
    def heartbeat_as_of(self, heartbeat_as_of):
        """Sets the heartbeat_as_of of this MarketStatus.

        The timestamp when the last heartbeat of the backend system has been received (should be not older than 5 seconds)  # noqa: E501

        :param heartbeat_as_of: The heartbeat_as_of of this MarketStatus.  # noqa: E501
        :type heartbeat_as_of: datetime
        """

        self._heartbeat_as_of = heartbeat_as_of

    @property
    def heartbeat_content(self):
        """Gets the heartbeat_content of this MarketStatus.  # noqa: E501

        The content of the last heartbeat  # noqa: E501

        :return: The heartbeat_content of this MarketStatus.  # noqa: E501
        :rtype: str
        """
        return self._heartbeat_content

    @heartbeat_content.setter
    def heartbeat_content(self, heartbeat_content):
        """Sets the heartbeat_content of this MarketStatus.

        The content of the last heartbeat  # noqa: E501

        :param heartbeat_content: The heartbeat_content of this MarketStatus.  # noqa: E501
        :type heartbeat_content: str
        """

        self._heartbeat_content = heartbeat_content

    @property
    def mfa_supported(self):
        """Gets the mfa_supported of this MarketStatus.  # noqa: E501

        Indicates whether the exchange supports multi-factor authentication  # noqa: E501

        :return: The mfa_supported of this MarketStatus.  # noqa: E501
        :rtype: bool
        """
        return self._mfa_supported

    @mfa_supported.setter
    def mfa_supported(self, mfa_supported):
        """Sets the mfa_supported of this MarketStatus.

        Indicates whether the exchange supports multi-factor authentication  # noqa: E501

        :param mfa_supported: The mfa_supported of this MarketStatus.  # noqa: E501
        :type mfa_supported: bool
        """

        self._mfa_supported = mfa_supported

    @property
    def mfa_secret(self):
        """Gets the mfa_secret of this MarketStatus.  # noqa: E501

        The MFA secret.  **Note**: only set when it was generated.  # noqa: E501

        :return: The mfa_secret of this MarketStatus.  # noqa: E501
        :rtype: str
        """
        return self._mfa_secret

    @mfa_secret.setter
    def mfa_secret(self, mfa_secret):
        """Sets the mfa_secret of this MarketStatus.

        The MFA secret.  **Note**: only set when it was generated.  # noqa: E501

        :param mfa_secret: The mfa_secret of this MarketStatus.  # noqa: E501
        :type mfa_secret: str
        """

        self._mfa_secret = mfa_secret

    @property
    def messages(self):
        """Gets the messages of this MarketStatus.  # noqa: E501

        Messages explaining the state of the market  # noqa: E501

        :return: The messages of this MarketStatus.  # noqa: E501
        :rtype: list[str]
        """
        return self._messages

    @messages.setter
    def messages(self, messages):
        """Sets the messages of this MarketStatus.

        Messages explaining the state of the market  # noqa: E501

        :param messages: The messages of this MarketStatus.  # noqa: E501
        :type messages: list[str]
        """

        self._messages = messages

    @property
    def mode(self):
        """Gets the mode of this MarketStatus.  # noqa: E501


        :return: The mode of this MarketStatus.  # noqa: E501
        :rtype: str
        """
        return self._mode

    @mode.setter
    def mode(self, mode):
        """Sets the mode of this MarketStatus.


        :param mode: The mode of this MarketStatus.  # noqa: E501
        :type mode: str
        """
        allowed_values = ["NORMAL", "SAFE"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and mode not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `mode` ({0}), must be one of {1}"  # noqa: E501
                .format(mode, allowed_values)
            )

        self._mode = mode

    @property
    def order_action_quota(self):
        """Gets the order_action_quota of this MarketStatus.  # noqa: E501

        **Only supported for EPEX, Nord Pool, IBEX and CROPEX**  The percentage (0.0 - 1.0) of consumed order entry/modification quota calculated depending on the underlying exchange.  This value is calculated based on the following formula:  `max{short_usage/short_limit, long_usage/long_limit}`  # noqa: E501

        :return: The order_action_quota of this MarketStatus.  # noqa: E501
        :rtype: float
        """
        return self._order_action_quota

    @order_action_quota.setter
    def order_action_quota(self, order_action_quota):
        """Sets the order_action_quota of this MarketStatus.

        **Only supported for EPEX, Nord Pool, IBEX and CROPEX**  The percentage (0.0 - 1.0) of consumed order entry/modification quota calculated depending on the underlying exchange.  This value is calculated based on the following formula:  `max{short_usage/short_limit, long_usage/long_limit}`  # noqa: E501

        :param order_action_quota: The order_action_quota of this MarketStatus.  # noqa: E501
        :type order_action_quota: float
        """

        self._order_action_quota = order_action_quota

    @property
    def available_account_ids(self):
        """Gets the available_account_ids of this MarketStatus.  # noqa: E501

        The available exchange account IDs  # noqa: E501

        :return: The available_account_ids of this MarketStatus.  # noqa: E501
        :rtype: list[str]
        """
        return self._available_account_ids

    @available_account_ids.setter
    def available_account_ids(self, available_account_ids):
        """Sets the available_account_ids of this MarketStatus.

        The available exchange account IDs  # noqa: E501

        :param available_account_ids: The available_account_ids of this MarketStatus.  # noqa: E501
        :type available_account_ids: list[str]
        """

        self._available_account_ids = available_account_ids

    @property
    def session_max_age(self):
        """Gets the session_max_age of this MarketStatus.  # noqa: E501

        Specifies the max age of the cookie in seconds. Note: If the cookie-max-age is set to a negative number, the cookie will be deleted when the browser is closed  # noqa: E501

        :return: The session_max_age of this MarketStatus.  # noqa: E501
        :rtype: int
        """
        return self._session_max_age

    @session_max_age.setter
    def session_max_age(self, session_max_age):
        """Sets the session_max_age of this MarketStatus.

        Specifies the max age of the cookie in seconds. Note: If the cookie-max-age is set to a negative number, the cookie will be deleted when the browser is closed  # noqa: E501

        :param session_max_age: The session_max_age of this MarketStatus.  # noqa: E501
        :type session_max_age: int
        """

        self._session_max_age = session_max_age

    @property
    def session_max_inactive_time(self):
        """Gets the session_max_inactive_time of this MarketStatus.  # noqa: E501

        Specifies the max time in seconds a session can be inactive before it is invalidated. Note: If the session-max-inactive-time is set to 0 or a negative number, the session will never expire  # noqa: E501

        :return: The session_max_inactive_time of this MarketStatus.  # noqa: E501
        :rtype: int
        """
        return self._session_max_inactive_time

    @session_max_inactive_time.setter
    def session_max_inactive_time(self, session_max_inactive_time):
        """Sets the session_max_inactive_time of this MarketStatus.

        Specifies the max time in seconds a session can be inactive before it is invalidated. Note: If the session-max-inactive-time is set to 0 or a negative number, the session will never expire  # noqa: E501

        :param session_max_inactive_time: The session_max_inactive_time of this MarketStatus.  # noqa: E501
        :type session_max_inactive_time: int
        """

        self._session_max_inactive_time = session_max_inactive_time

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, MarketStatus):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, MarketStatus):
            return True

        return self.to_dict() != other.to_dict()
