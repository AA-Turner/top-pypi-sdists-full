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


class OrderBooks(object):
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
        'delivery_area': 'str',
        'delivery_area_state': 'str',
        'market_area_state': 'str',
        'portfolios': 'list[str]',
        'products': 'list[ProductInformation]',
        'contracts': 'list[Contract]',
        'orders': 'list[Orders]',
        'portfolio_risk_settings': 'list[RiskManagementSettings]',
        'tenant_risk_settings': 'RiskManagementSettings'
    }

    attribute_map = {
        'delivery_area': 'delivery_area',
        'delivery_area_state': 'delivery_area_state',
        'market_area_state': 'market_area_state',
        'portfolios': 'portfolios',
        'products': 'products',
        'contracts': 'contracts',
        'orders': 'orders',
        'portfolio_risk_settings': 'portfolio_risk_settings',
        'tenant_risk_settings': 'tenant_risk_settings'
    }

    def __init__(self, delivery_area=None, delivery_area_state=None, market_area_state=None, portfolios=None, products=None, contracts=None, orders=None, portfolio_risk_settings=None, tenant_risk_settings=None, local_vars_configuration=None):  # noqa: E501
        """OrderBooks - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._delivery_area = None
        self._delivery_area_state = None
        self._market_area_state = None
        self._portfolios = None
        self._products = None
        self._contracts = None
        self._orders = None
        self._portfolio_risk_settings = None
        self._tenant_risk_settings = None
        self.discriminator = None

        if delivery_area is not None:
            self.delivery_area = delivery_area
        if delivery_area_state is not None:
            self.delivery_area_state = delivery_area_state
        if market_area_state is not None:
            self.market_area_state = market_area_state
        if portfolios is not None:
            self.portfolios = portfolios
        if products is not None:
            self.products = products
        if contracts is not None:
            self.contracts = contracts
        if orders is not None:
            self.orders = orders
        if portfolio_risk_settings is not None:
            self.portfolio_risk_settings = portfolio_risk_settings
        if tenant_risk_settings is not None:
            self.tenant_risk_settings = tenant_risk_settings

    @property
    def delivery_area(self):
        """Gets the delivery_area of this OrderBooks.  # noqa: E501


        :return: The delivery_area of this OrderBooks.  # noqa: E501
        :rtype: str
        """
        return self._delivery_area

    @delivery_area.setter
    def delivery_area(self, delivery_area):
        """Sets the delivery_area of this OrderBooks.


        :param delivery_area: The delivery_area of this OrderBooks.  # noqa: E501
        :type delivery_area: str
        """

        self._delivery_area = delivery_area

    @property
    def delivery_area_state(self):
        """Gets the delivery_area_state of this OrderBooks.  # noqa: E501


        :return: The delivery_area_state of this OrderBooks.  # noqa: E501
        :rtype: str
        """
        return self._delivery_area_state

    @delivery_area_state.setter
    def delivery_area_state(self, delivery_area_state):
        """Sets the delivery_area_state of this OrderBooks.


        :param delivery_area_state: The delivery_area_state of this OrderBooks.  # noqa: E501
        :type delivery_area_state: str
        """

        self._delivery_area_state = delivery_area_state

    @property
    def market_area_state(self):
        """Gets the market_area_state of this OrderBooks.  # noqa: E501


        :return: The market_area_state of this OrderBooks.  # noqa: E501
        :rtype: str
        """
        return self._market_area_state

    @market_area_state.setter
    def market_area_state(self, market_area_state):
        """Sets the market_area_state of this OrderBooks.


        :param market_area_state: The market_area_state of this OrderBooks.  # noqa: E501
        :type market_area_state: str
        """

        self._market_area_state = market_area_state

    @property
    def portfolios(self):
        """Gets the portfolios of this OrderBooks.  # noqa: E501


        :return: The portfolios of this OrderBooks.  # noqa: E501
        :rtype: list[str]
        """
        return self._portfolios

    @portfolios.setter
    def portfolios(self, portfolios):
        """Sets the portfolios of this OrderBooks.


        :param portfolios: The portfolios of this OrderBooks.  # noqa: E501
        :type portfolios: list[str]
        """

        self._portfolios = portfolios

    @property
    def products(self):
        """Gets the products of this OrderBooks.  # noqa: E501

        The involved products of the orderbooks  # noqa: E501

        :return: The products of this OrderBooks.  # noqa: E501
        :rtype: list[ProductInformation]
        """
        return self._products

    @products.setter
    def products(self, products):
        """Sets the products of this OrderBooks.

        The involved products of the orderbooks  # noqa: E501

        :param products: The products of this OrderBooks.  # noqa: E501
        :type products: list[ProductInformation]
        """

        self._products = products

    @property
    def contracts(self):
        """Gets the contracts of this OrderBooks.  # noqa: E501

        The contracts of the orderbooks  # noqa: E501

        :return: The contracts of this OrderBooks.  # noqa: E501
        :rtype: list[Contract]
        """
        return self._contracts

    @contracts.setter
    def contracts(self, contracts):
        """Sets the contracts of this OrderBooks.

        The contracts of the orderbooks  # noqa: E501

        :param contracts: The contracts of this OrderBooks.  # noqa: E501
        :type contracts: list[Contract]
        """

        self._contracts = contracts

    @property
    def orders(self):
        """Gets the orders of this OrderBooks.  # noqa: E501


        :return: The orders of this OrderBooks.  # noqa: E501
        :rtype: list[Orders]
        """
        return self._orders

    @orders.setter
    def orders(self, orders):
        """Sets the orders of this OrderBooks.


        :param orders: The orders of this OrderBooks.  # noqa: E501
        :type orders: list[Orders]
        """

        self._orders = orders

    @property
    def portfolio_risk_settings(self):
        """Gets the portfolio_risk_settings of this OrderBooks.  # noqa: E501


        :return: The portfolio_risk_settings of this OrderBooks.  # noqa: E501
        :rtype: list[RiskManagementSettings]
        """
        return self._portfolio_risk_settings

    @portfolio_risk_settings.setter
    def portfolio_risk_settings(self, portfolio_risk_settings):
        """Sets the portfolio_risk_settings of this OrderBooks.


        :param portfolio_risk_settings: The portfolio_risk_settings of this OrderBooks.  # noqa: E501
        :type portfolio_risk_settings: list[RiskManagementSettings]
        """

        self._portfolio_risk_settings = portfolio_risk_settings

    @property
    def tenant_risk_settings(self):
        """Gets the tenant_risk_settings of this OrderBooks.  # noqa: E501


        :return: The tenant_risk_settings of this OrderBooks.  # noqa: E501
        :rtype: RiskManagementSettings
        """
        return self._tenant_risk_settings

    @tenant_risk_settings.setter
    def tenant_risk_settings(self, tenant_risk_settings):
        """Sets the tenant_risk_settings of this OrderBooks.


        :param tenant_risk_settings: The tenant_risk_settings of this OrderBooks.  # noqa: E501
        :type tenant_risk_settings: RiskManagementSettings
        """

        self._tenant_risk_settings = tenant_risk_settings

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
        if not isinstance(other, OrderBooks):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OrderBooks):
            return True

        return self.to_dict() != other.to_dict()
