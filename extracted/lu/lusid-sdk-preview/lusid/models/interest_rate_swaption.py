# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 1.1.257
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from lusid.configuration import Configuration


class InterestRateSwaption(object):
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
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'start_date': 'datetime',
        'pay_or_receive_fixed': 'str',
        'premium': 'Premium',
        'delivery_method': 'str',
        'swap': 'InterestRateSwap',
        'instrument_type': 'str'
    }

    attribute_map = {
        'start_date': 'startDate',
        'pay_or_receive_fixed': 'payOrReceiveFixed',
        'premium': 'premium',
        'delivery_method': 'deliveryMethod',
        'swap': 'swap',
        'instrument_type': 'instrumentType'
    }

    required_map = {
        'start_date': 'required',
        'pay_or_receive_fixed': 'required',
        'premium': 'optional',
        'delivery_method': 'required',
        'swap': 'required',
        'instrument_type': 'required'
    }

    def __init__(self, start_date=None, pay_or_receive_fixed=None, premium=None, delivery_method=None, swap=None, instrument_type=None, local_vars_configuration=None):  # noqa: E501
        """InterestRateSwaption - a model defined in OpenAPI"
        
        :param start_date:  The start date of the instrument. This is normally synonymous with the trade-date. (required)
        :type start_date: datetime
        :param pay_or_receive_fixed:  True if on exercise the holder of the option enters the swap paying fixed, false if floating.    Supported string (enumeration) values are: [Pay, Receive]. (required)
        :type pay_or_receive_fixed: str
        :param premium: 
        :type premium: lusid.Premium
        :param delivery_method:  How does the option settle    Supported string (enumeration) values are: [Cash, Physical]. (required)
        :type delivery_method: str
        :param swap:  (required)
        :type swap: lusid.InterestRateSwap
        :param instrument_type:  The available values are: QuotedSecurity, InterestRateSwap, FxForward, Future, ExoticInstrument, FxOption, CreditDefaultSwap, InterestRateSwaption, Bond, EquityOption, FixedLeg, FloatingLeg, BespokeCashFlowsLeg, Unknown, TermDeposit, ContractForDifference, EquitySwap, CashPerpetual, CapFloor, CashSettled, CdsIndex, Basket, FundingLeg, FxSwap, ForwardRateAgreement, SimpleInstrument, Repo, Equity, ExchangeTradedOption, ReferenceInstrument, ComplexBond, InflationLinkedBond, InflationSwap, SimpleCashFlowLoan, TotalReturnSwap, InflationLeg, FundShareClass, FlexibleLoan, UnsettledCash, Cash, MasteredInstrument, LoanFacility (required)
        :type instrument_type: str

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._start_date = None
        self._pay_or_receive_fixed = None
        self._premium = None
        self._delivery_method = None
        self._swap = None
        self._instrument_type = None
        self.discriminator = None

        self.start_date = start_date
        self.pay_or_receive_fixed = pay_or_receive_fixed
        if premium is not None:
            self.premium = premium
        self.delivery_method = delivery_method
        self.swap = swap
        self.instrument_type = instrument_type

    @property
    def start_date(self):
        """Gets the start_date of this InterestRateSwaption.  # noqa: E501

        The start date of the instrument. This is normally synonymous with the trade-date.  # noqa: E501

        :return: The start_date of this InterestRateSwaption.  # noqa: E501
        :rtype: datetime
        """
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        """Sets the start_date of this InterestRateSwaption.

        The start date of the instrument. This is normally synonymous with the trade-date.  # noqa: E501

        :param start_date: The start_date of this InterestRateSwaption.  # noqa: E501
        :type start_date: datetime
        """
        if self.local_vars_configuration.client_side_validation and start_date is None:  # noqa: E501
            raise ValueError("Invalid value for `start_date`, must not be `None`")  # noqa: E501

        self._start_date = start_date

    @property
    def pay_or_receive_fixed(self):
        """Gets the pay_or_receive_fixed of this InterestRateSwaption.  # noqa: E501

        True if on exercise the holder of the option enters the swap paying fixed, false if floating.    Supported string (enumeration) values are: [Pay, Receive].  # noqa: E501

        :return: The pay_or_receive_fixed of this InterestRateSwaption.  # noqa: E501
        :rtype: str
        """
        return self._pay_or_receive_fixed

    @pay_or_receive_fixed.setter
    def pay_or_receive_fixed(self, pay_or_receive_fixed):
        """Sets the pay_or_receive_fixed of this InterestRateSwaption.

        True if on exercise the holder of the option enters the swap paying fixed, false if floating.    Supported string (enumeration) values are: [Pay, Receive].  # noqa: E501

        :param pay_or_receive_fixed: The pay_or_receive_fixed of this InterestRateSwaption.  # noqa: E501
        :type pay_or_receive_fixed: str
        """
        if self.local_vars_configuration.client_side_validation and pay_or_receive_fixed is None:  # noqa: E501
            raise ValueError("Invalid value for `pay_or_receive_fixed`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                pay_or_receive_fixed is not None and len(pay_or_receive_fixed) < 1):
            raise ValueError("Invalid value for `pay_or_receive_fixed`, length must be greater than or equal to `1`")  # noqa: E501

        self._pay_or_receive_fixed = pay_or_receive_fixed

    @property
    def premium(self):
        """Gets the premium of this InterestRateSwaption.  # noqa: E501


        :return: The premium of this InterestRateSwaption.  # noqa: E501
        :rtype: lusid.Premium
        """
        return self._premium

    @premium.setter
    def premium(self, premium):
        """Sets the premium of this InterestRateSwaption.


        :param premium: The premium of this InterestRateSwaption.  # noqa: E501
        :type premium: lusid.Premium
        """

        self._premium = premium

    @property
    def delivery_method(self):
        """Gets the delivery_method of this InterestRateSwaption.  # noqa: E501

        How does the option settle    Supported string (enumeration) values are: [Cash, Physical].  # noqa: E501

        :return: The delivery_method of this InterestRateSwaption.  # noqa: E501
        :rtype: str
        """
        return self._delivery_method

    @delivery_method.setter
    def delivery_method(self, delivery_method):
        """Sets the delivery_method of this InterestRateSwaption.

        How does the option settle    Supported string (enumeration) values are: [Cash, Physical].  # noqa: E501

        :param delivery_method: The delivery_method of this InterestRateSwaption.  # noqa: E501
        :type delivery_method: str
        """
        if self.local_vars_configuration.client_side_validation and delivery_method is None:  # noqa: E501
            raise ValueError("Invalid value for `delivery_method`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                delivery_method is not None and len(delivery_method) < 1):
            raise ValueError("Invalid value for `delivery_method`, length must be greater than or equal to `1`")  # noqa: E501

        self._delivery_method = delivery_method

    @property
    def swap(self):
        """Gets the swap of this InterestRateSwaption.  # noqa: E501


        :return: The swap of this InterestRateSwaption.  # noqa: E501
        :rtype: lusid.InterestRateSwap
        """
        return self._swap

    @swap.setter
    def swap(self, swap):
        """Sets the swap of this InterestRateSwaption.


        :param swap: The swap of this InterestRateSwaption.  # noqa: E501
        :type swap: lusid.InterestRateSwap
        """
        if self.local_vars_configuration.client_side_validation and swap is None:  # noqa: E501
            raise ValueError("Invalid value for `swap`, must not be `None`")  # noqa: E501

        self._swap = swap

    @property
    def instrument_type(self):
        """Gets the instrument_type of this InterestRateSwaption.  # noqa: E501

        The available values are: QuotedSecurity, InterestRateSwap, FxForward, Future, ExoticInstrument, FxOption, CreditDefaultSwap, InterestRateSwaption, Bond, EquityOption, FixedLeg, FloatingLeg, BespokeCashFlowsLeg, Unknown, TermDeposit, ContractForDifference, EquitySwap, CashPerpetual, CapFloor, CashSettled, CdsIndex, Basket, FundingLeg, FxSwap, ForwardRateAgreement, SimpleInstrument, Repo, Equity, ExchangeTradedOption, ReferenceInstrument, ComplexBond, InflationLinkedBond, InflationSwap, SimpleCashFlowLoan, TotalReturnSwap, InflationLeg, FundShareClass, FlexibleLoan, UnsettledCash, Cash, MasteredInstrument, LoanFacility  # noqa: E501

        :return: The instrument_type of this InterestRateSwaption.  # noqa: E501
        :rtype: str
        """
        return self._instrument_type

    @instrument_type.setter
    def instrument_type(self, instrument_type):
        """Sets the instrument_type of this InterestRateSwaption.

        The available values are: QuotedSecurity, InterestRateSwap, FxForward, Future, ExoticInstrument, FxOption, CreditDefaultSwap, InterestRateSwaption, Bond, EquityOption, FixedLeg, FloatingLeg, BespokeCashFlowsLeg, Unknown, TermDeposit, ContractForDifference, EquitySwap, CashPerpetual, CapFloor, CashSettled, CdsIndex, Basket, FundingLeg, FxSwap, ForwardRateAgreement, SimpleInstrument, Repo, Equity, ExchangeTradedOption, ReferenceInstrument, ComplexBond, InflationLinkedBond, InflationSwap, SimpleCashFlowLoan, TotalReturnSwap, InflationLeg, FundShareClass, FlexibleLoan, UnsettledCash, Cash, MasteredInstrument, LoanFacility  # noqa: E501

        :param instrument_type: The instrument_type of this InterestRateSwaption.  # noqa: E501
        :type instrument_type: str
        """
        if self.local_vars_configuration.client_side_validation and instrument_type is None:  # noqa: E501
            raise ValueError("Invalid value for `instrument_type`, must not be `None`")  # noqa: E501
        allowed_values = ["QuotedSecurity", "InterestRateSwap", "FxForward", "Future", "ExoticInstrument", "FxOption", "CreditDefaultSwap", "InterestRateSwaption", "Bond", "EquityOption", "FixedLeg", "FloatingLeg", "BespokeCashFlowsLeg", "Unknown", "TermDeposit", "ContractForDifference", "EquitySwap", "CashPerpetual", "CapFloor", "CashSettled", "CdsIndex", "Basket", "FundingLeg", "FxSwap", "ForwardRateAgreement", "SimpleInstrument", "Repo", "Equity", "ExchangeTradedOption", "ReferenceInstrument", "ComplexBond", "InflationLinkedBond", "InflationSwap", "SimpleCashFlowLoan", "TotalReturnSwap", "InflationLeg", "FundShareClass", "FlexibleLoan", "UnsettledCash", "Cash", "MasteredInstrument", "LoanFacility"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and instrument_type not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `instrument_type` ({0}), must be one of {1}"  # noqa: E501
                .format(instrument_type, allowed_values)
            )

        self._instrument_type = instrument_type

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
        if not isinstance(other, InterestRateSwaption):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InterestRateSwaption):
            return True

        return self.to_dict() != other.to_dict()
