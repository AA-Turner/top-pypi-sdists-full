# coding: utf-8

"""
    Aron API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from openapi_client.configuration import Configuration


class OrmProjectDashboardChartSection(object):
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
        'column_count': 'int',
        'created_dt': 'datetime',
        'dashboard_id': 'int',
        'edges': 'OrmProjectDashboardChartSectionEdges',
        'id': 'int',
        'is_collapsed': 'bool',
        'name': 'str',
        'order': 'int',
        'smoothing': 'float',
        'type': 'str',
        'updated_dt': 'datetime',
        'x_axis': 'str',
        'x_axis_max': 'float',
        'x_axis_min': 'float'
    }

    attribute_map = {
        'column_count': 'column_count',
        'created_dt': 'created_dt',
        'dashboard_id': 'dashboard_id',
        'edges': 'edges',
        'id': 'id',
        'is_collapsed': 'is_collapsed',
        'name': 'name',
        'order': 'order',
        'smoothing': 'smoothing',
        'type': 'type',
        'updated_dt': 'updated_dt',
        'x_axis': 'x_axis',
        'x_axis_max': 'x_axis_max',
        'x_axis_min': 'x_axis_min'
    }

    def __init__(self, column_count=None, created_dt=None, dashboard_id=None, edges=None, id=None, is_collapsed=None, name=None, order=None, smoothing=None, type=None, updated_dt=None, x_axis=None, x_axis_max=None, x_axis_min=None, local_vars_configuration=None):  # noqa: E501
        """OrmProjectDashboardChartSection - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._column_count = None
        self._created_dt = None
        self._dashboard_id = None
        self._edges = None
        self._id = None
        self._is_collapsed = None
        self._name = None
        self._order = None
        self._smoothing = None
        self._type = None
        self._updated_dt = None
        self._x_axis = None
        self._x_axis_max = None
        self._x_axis_min = None
        self.discriminator = None

        if column_count is not None:
            self.column_count = column_count
        if created_dt is not None:
            self.created_dt = created_dt
        if dashboard_id is not None:
            self.dashboard_id = dashboard_id
        if edges is not None:
            self.edges = edges
        if id is not None:
            self.id = id
        if is_collapsed is not None:
            self.is_collapsed = is_collapsed
        if name is not None:
            self.name = name
        self.order = order
        self.smoothing = smoothing
        self.type = type
        if updated_dt is not None:
            self.updated_dt = updated_dt
        self.x_axis = x_axis
        self.x_axis_max = x_axis_max
        self.x_axis_min = x_axis_min

    @property
    def column_count(self):
        """Gets the column_count of this OrmProjectDashboardChartSection.  # noqa: E501


        :return: The column_count of this OrmProjectDashboardChartSection.  # noqa: E501
        :rtype: int
        """
        return self._column_count

    @column_count.setter
    def column_count(self, column_count):
        """Sets the column_count of this OrmProjectDashboardChartSection.


        :param column_count: The column_count of this OrmProjectDashboardChartSection.  # noqa: E501
        :type column_count: int
        """

        self._column_count = column_count

    @property
    def created_dt(self):
        """Gets the created_dt of this OrmProjectDashboardChartSection.  # noqa: E501


        :return: The created_dt of this OrmProjectDashboardChartSection.  # noqa: E501
        :rtype: datetime
        """
        return self._created_dt

    @created_dt.setter
    def created_dt(self, created_dt):
        """Sets the created_dt of this OrmProjectDashboardChartSection.


        :param created_dt: The created_dt of this OrmProjectDashboardChartSection.  # noqa: E501
        :type created_dt: datetime
        """

        self._created_dt = created_dt

    @property
    def dashboard_id(self):
        """Gets the dashboard_id of this OrmProjectDashboardChartSection.  # noqa: E501


        :return: The dashboard_id of this OrmProjectDashboardChartSection.  # noqa: E501
        :rtype: int
        """
        return self._dashboard_id

    @dashboard_id.setter
    def dashboard_id(self, dashboard_id):
        """Sets the dashboard_id of this OrmProjectDashboardChartSection.


        :param dashboard_id: The dashboard_id of this OrmProjectDashboardChartSection.  # noqa: E501
        :type dashboard_id: int
        """

        self._dashboard_id = dashboard_id

    @property
    def edges(self):
        """Gets the edges of this OrmProjectDashboardChartSection.  # noqa: E501


        :return: The edges of this OrmProjectDashboardChartSection.  # noqa: E501
        :rtype: OrmProjectDashboardChartSectionEdges
        """
        return self._edges

    @edges.setter
    def edges(self, edges):
        """Sets the edges of this OrmProjectDashboardChartSection.


        :param edges: The edges of this OrmProjectDashboardChartSection.  # noqa: E501
        :type edges: OrmProjectDashboardChartSectionEdges
        """

        self._edges = edges

    @property
    def id(self):
        """Gets the id of this OrmProjectDashboardChartSection.  # noqa: E501


        :return: The id of this OrmProjectDashboardChartSection.  # noqa: E501
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this OrmProjectDashboardChartSection.


        :param id: The id of this OrmProjectDashboardChartSection.  # noqa: E501
        :type id: int
        """

        self._id = id

    @property
    def is_collapsed(self):
        """Gets the is_collapsed of this OrmProjectDashboardChartSection.  # noqa: E501


        :return: The is_collapsed of this OrmProjectDashboardChartSection.  # noqa: E501
        :rtype: bool
        """
        return self._is_collapsed

    @is_collapsed.setter
    def is_collapsed(self, is_collapsed):
        """Sets the is_collapsed of this OrmProjectDashboardChartSection.


        :param is_collapsed: The is_collapsed of this OrmProjectDashboardChartSection.  # noqa: E501
        :type is_collapsed: bool
        """

        self._is_collapsed = is_collapsed

    @property
    def name(self):
        """Gets the name of this OrmProjectDashboardChartSection.  # noqa: E501


        :return: The name of this OrmProjectDashboardChartSection.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this OrmProjectDashboardChartSection.


        :param name: The name of this OrmProjectDashboardChartSection.  # noqa: E501
        :type name: str
        """

        self._name = name

    @property
    def order(self):
        """Gets the order of this OrmProjectDashboardChartSection.  # noqa: E501


        :return: The order of this OrmProjectDashboardChartSection.  # noqa: E501
        :rtype: int
        """
        return self._order

    @order.setter
    def order(self, order):
        """Sets the order of this OrmProjectDashboardChartSection.


        :param order: The order of this OrmProjectDashboardChartSection.  # noqa: E501
        :type order: int
        """

        self._order = order

    @property
    def smoothing(self):
        """Gets the smoothing of this OrmProjectDashboardChartSection.  # noqa: E501


        :return: The smoothing of this OrmProjectDashboardChartSection.  # noqa: E501
        :rtype: float
        """
        return self._smoothing

    @smoothing.setter
    def smoothing(self, smoothing):
        """Sets the smoothing of this OrmProjectDashboardChartSection.


        :param smoothing: The smoothing of this OrmProjectDashboardChartSection.  # noqa: E501
        :type smoothing: float
        """

        self._smoothing = smoothing

    @property
    def type(self):
        """Gets the type of this OrmProjectDashboardChartSection.  # noqa: E501


        :return: The type of this OrmProjectDashboardChartSection.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this OrmProjectDashboardChartSection.


        :param type: The type of this OrmProjectDashboardChartSection.  # noqa: E501
        :type type: str
        """

        self._type = type

    @property
    def updated_dt(self):
        """Gets the updated_dt of this OrmProjectDashboardChartSection.  # noqa: E501


        :return: The updated_dt of this OrmProjectDashboardChartSection.  # noqa: E501
        :rtype: datetime
        """
        return self._updated_dt

    @updated_dt.setter
    def updated_dt(self, updated_dt):
        """Sets the updated_dt of this OrmProjectDashboardChartSection.


        :param updated_dt: The updated_dt of this OrmProjectDashboardChartSection.  # noqa: E501
        :type updated_dt: datetime
        """

        self._updated_dt = updated_dt

    @property
    def x_axis(self):
        """Gets the x_axis of this OrmProjectDashboardChartSection.  # noqa: E501


        :return: The x_axis of this OrmProjectDashboardChartSection.  # noqa: E501
        :rtype: str
        """
        return self._x_axis

    @x_axis.setter
    def x_axis(self, x_axis):
        """Sets the x_axis of this OrmProjectDashboardChartSection.


        :param x_axis: The x_axis of this OrmProjectDashboardChartSection.  # noqa: E501
        :type x_axis: str
        """

        self._x_axis = x_axis

    @property
    def x_axis_max(self):
        """Gets the x_axis_max of this OrmProjectDashboardChartSection.  # noqa: E501


        :return: The x_axis_max of this OrmProjectDashboardChartSection.  # noqa: E501
        :rtype: float
        """
        return self._x_axis_max

    @x_axis_max.setter
    def x_axis_max(self, x_axis_max):
        """Sets the x_axis_max of this OrmProjectDashboardChartSection.


        :param x_axis_max: The x_axis_max of this OrmProjectDashboardChartSection.  # noqa: E501
        :type x_axis_max: float
        """

        self._x_axis_max = x_axis_max

    @property
    def x_axis_min(self):
        """Gets the x_axis_min of this OrmProjectDashboardChartSection.  # noqa: E501


        :return: The x_axis_min of this OrmProjectDashboardChartSection.  # noqa: E501
        :rtype: float
        """
        return self._x_axis_min

    @x_axis_min.setter
    def x_axis_min(self, x_axis_min):
        """Sets the x_axis_min of this OrmProjectDashboardChartSection.


        :param x_axis_min: The x_axis_min of this OrmProjectDashboardChartSection.  # noqa: E501
        :type x_axis_min: float
        """

        self._x_axis_min = x_axis_min

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
        if not isinstance(other, OrmProjectDashboardChartSection):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OrmProjectDashboardChartSection):
            return True

        return self.to_dict() != other.to_dict()
