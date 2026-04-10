# -*- coding: utf8 -*-

from tablestore.metadata import *
from tablestore.plainbuffer.plain_buffer_builder import * 
import tablestore.protobuf.search_pb2 as search_pb2

class BaseGroupBy(object):
    def __init__(self, field_name, sub_aggs, sub_group_bys, name, type):
        self.field_name = field_name
        self.sub_aggs = sub_aggs
        self.sub_group_bys = sub_group_bys
        self.name = name
        self.type = type

    def add_sub_agg(self, agg):
        self.sub_aggs.append(agg)

    def add_sub_group_by(self, group_by):
        self.sub_group_bys.append(group_by)

    def to_pb_str(self, agg_encode_func, group_by_encode_func, query_encode_func):
        pass

    def _base_to_pb_str(self, proto, agg_encode_func, group_by_encode_func):
        if self.field_name is not None:
            proto.field_name = self.field_name

        if self.sub_aggs is not None:
            agg_encode_func(proto.sub_aggs, self.sub_aggs)

        if self.sub_group_bys is not None:
            group_by_encode_func(proto.sub_group_bys, self.sub_group_bys)

    def range_to_pb(self, ranges, r):
        range_proto = ranges.add()
        begin, end = r[0], r[1]
        if isinstance(begin, (six.integer_types, float)) and isinstance(end, (six.integer_types,float)):
            range_proto.begin = begin
            range_proto.end = end
        else:
            raise OTSClientError('range.begin and range.end must be integer or float')

class GroupKeySort(object):
    def __init__(self, sort_order):
        self.sort_order = sort_order
        
    
class RowCountSort(object):
    def __init__(self, sort_order):
        self.sort_order = sort_order


class SubAggSort(object):
    def __init__(self, sort_order, sub_agg_name):
        self.sort_order = sort_order
        self.sub_agg_name = sub_agg_name

class GroupByField(BaseGroupBy):

    def __init__(self, field_name, size = None, group_by_sort = None, sub_aggs = None, sub_group_bys = None, name = 'group_by_field'):
        sub_aggs = [] if sub_aggs is None else sub_aggs[:]
        sub_group_bys = [] if sub_group_bys is None else sub_group_bys[:]
        BaseGroupBy.__init__(self, field_name, sub_aggs, sub_group_bys, name, search_pb2.GROUP_BY_FIELD)
        
        self.size = size
        self.group_by_sort = group_by_sort
        self.sub_aggs = sub_aggs
        self.sub_group_bys = sub_group_bys

    def to_pb_str(self, agg_encode_func, group_by_encode_func, query_encode_func):
        proto = search_pb2.GroupByField()
        if self.size is not None:
            if isinstance(self.size, int):
                proto.size = self.size
            else:
                raise OTSClientError('size must be integer')

        if self.group_by_sort is not None:
            if isinstance(self.group_by_sort, list):
                for sort in self.group_by_sort:
                    if isinstance(sort, GroupKeySort):
                        sorter = proto.sort.sorters.add()
                        sorter.group_key_sort.order = self._get_enum(sort.sort_order)
                    elif isinstance(sort, RowCountSort):
                        sorter = proto.sort.sorters.add()
                        sorter.row_count_sort.order = self._get_enum(sort.sort_order)
                    elif isinstance(sort, SubAggSort):
                        sorter = proto.sort.sorters.add()
                        sorter.sub_agg_sort.order = self._get_enum(sort.sort_order)
                        sorter.sub_agg_sort.sub_agg_name = sort.sub_agg_name
                    else:
                        raise OTSClientError('Invalid sort type:%s' % str(type(sort)))
            else:
                raise OTSClientError('group_by_sort must be list')

        BaseGroupBy._base_to_pb_str(self, proto, agg_encode_func, group_by_encode_func)
        return proto.SerializeToString()

    def _get_enum(self, e):
        # to compatible with enum and enum34
        return e.value if hasattr(e, 'value') else e

class GroupByRange(BaseGroupBy):

    def __init__(self, field_name, ranges, sub_aggs = None, sub_group_bys = None, name = 'group_by_range'):
        sub_aggs = [] if sub_aggs is None else sub_aggs[:]
        sub_group_bys = [] if sub_group_bys is None else sub_group_bys[:]
        BaseGroupBy.__init__(self, field_name, sub_aggs, sub_group_bys, name, search_pb2.GROUP_BY_RANGE)
        self.ranges = ranges

    def add_range(self, range):
        self.ranges.append(range)

    def to_pb_str(self, agg_encode_func, group_by_encode_func, query_encode_func):
        proto = search_pb2.GroupByRange()
        
        if self.ranges is not None and isinstance(self.ranges, list):
            for r in self.ranges:
                if isinstance(r, tuple) and len(r) == 2:
                    self.range_to_pb(proto.ranges, r)
                else:
                    raise OTSClientError('GroupByRange:range must be tuple, and length must equal 2')
        else:
            raise OTSClientError('GroupByRange:ranges must be list')

        BaseGroupBy._base_to_pb_str(self, proto, agg_encode_func, group_by_encode_func)
        return proto.SerializeToString()

class GroupByFilter(BaseGroupBy):
    
    def __init__(self, filters, sub_aggs = None, sub_group_bys = None, name = 'group_by_filter'):
        sub_aggs = [] if sub_aggs is None else sub_aggs[:]
        sub_group_bys = [] if sub_group_bys is None else sub_group_bys[:]
        BaseGroupBy.__init__(self, None, sub_aggs, sub_group_bys, name, search_pb2.GROUP_BY_FILTER)

        self.filters = filters

    def add_filter(self, filter):
        self.filters.append(filter)

    def to_pb_str(self, agg_encode_func, group_by_encode_func, query_encode_func):
        proto = search_pb2.GroupByFilter()
        
        if self.filters is not None and isinstance(self.filters, list):
            for filter in self.filters:
                if isinstance(filter, Query):
                    query_encode_func(proto.filters.add(), filter)
                else:
                    raise OTSClientError('GroupByFilter:filter must be Query')
        else:
            raise OTSClientError('GroupByFilter:filters must be list')

        BaseGroupBy._base_to_pb_str(self, proto, agg_encode_func, group_by_encode_func)
        return proto.SerializeToString()

class GeoPoint(object):
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

class GroupByGeoDistance(BaseGroupBy):

    def __init__(self, field_name, origin, ranges, sub_aggs = None, sub_group_bys = None, name = 'group_by_geo_distance'):
        sub_aggs = [] if sub_aggs is None else sub_aggs[:]
        sub_group_bys = [] if sub_group_bys is None else sub_group_bys[:]
        BaseGroupBy.__init__(self, field_name, sub_aggs, sub_group_bys, name, search_pb2.GROUP_BY_GEO_DISTANCE)

        self.origin = origin
        self.ranges = ranges

    def add_range(self, range):
        self.ranges.append(range)

    def to_pb_str(self, agg_encode_func, group_by_encode_func, query_encode_func):
        proto = search_pb2.GroupByGeoDistance()

        if self.origin is not None and isinstance(self.origin, GeoPoint):
            proto.origin.lat = self.origin.lat
            proto.origin.lon = self.origin.lon
        else:
            raise OTSClientError('GroupByGeoDistance:origin must not be None and must be GeoPoint')
        
        if self.ranges is not None and isinstance(self.ranges, list):
            for range in self.ranges:
                if isinstance(range, tuple) and len(range) == 2:
                    self.range_to_pb(proto.ranges, range)
                else:
                    raise OTSClientError('GroupByGeoDistance:range must be tuple, and length must equal 2')
        else:
            raise OTSClientError('GroupByGeoDistance:ranges must be list')

        BaseGroupBy._base_to_pb_str(self, proto, agg_encode_func, group_by_encode_func)
        return proto.SerializeToString()

class FieldRange(object):
    def __init__(self, min, max):
        self.min = min
        self.max = max

class GroupByHistogram(BaseGroupBy):
    
    def __init__(self, field_name, interval, field_range, missing_value=None, min_doc_count=None, group_by_sort=None,
                 sub_aggs=None, sub_group_bys=None, name='group_by_histogram'):
        sub_aggs = [] if sub_aggs is None else sub_aggs[:]
        sub_group_bys = [] if sub_group_bys is None else sub_group_bys[:]
        BaseGroupBy.__init__(self, field_name, sub_aggs, sub_group_bys, name, search_pb2.GROUP_BY_HISTOGRAM)

        self.interval = interval
        self.field_range = field_range
        self.missing_value = missing_value
        self.min_doc_count = min_doc_count
        self.group_by_sort = group_by_sort

    def to_pb_str(self, agg_encode_func, group_by_encode_func, query_encode_func):
        proto = search_pb2.GroupByHistogram()

        if self.interval is not None:
            proto.interval = bytes(PlainBufferBuilder.serialize_column_value(self.interval))

        if self.missing_value is not None:
            proto.missing_value = bytes(PlainBufferBuilder.serialize_column_value(self.missing_value))

        if self.min_doc_count is not None:
            if isinstance(self.min_doc_count, int):
                proto.min_doc_count = self.min_doc_count
            else:
                raise OTSClientError('min_doc_count must be integer')

        if self.field_range is not None and self.field_range.min is not None and self.field_range.max is not None:
            proto.field_range.min = bytes(PlainBufferBuilder.serialize_column_value(self.field_range.min)) 
            proto.field_range.max = bytes(PlainBufferBuilder.serialize_column_value(self.field_range.max)) 
        else:
            raise OTSClientError('field_range(min, max) must not be None')

        if self.group_by_sort is not None:
            if isinstance(self.group_by_sort, list):
                for sort in self.group_by_sort:
                    if isinstance(sort, GroupKeySort):
                        sorter = proto.sort.sorters.add()
                        sorter.group_key_sort.order = self._get_enum(sort.sort_order)
                    elif isinstance(sort, RowCountSort):
                        sorter = proto.sort.sorters.add()
                        sorter.row_count_sort.order = self._get_enum(sort.sort_order)
                    elif isinstance(sort, SubAggSort):
                        sorter = proto.sort.sorters.add()
                        sorter.sub_agg_sort.order = self._get_enum(sort.sort_order)
                        sorter.sub_agg_sort.sub_agg_name = sort.sub_agg_name
                    else:
                        raise OTSClientError('Invalid sort type:%s' % str(type(sort)))
            else:
                raise OTSClientError('group_by_sort must be list')

        BaseGroupBy._base_to_pb_str(self, proto, agg_encode_func, group_by_encode_func)
        return proto.SerializeToString()

class GroupByResult(object):
    def __init__(self, name, items, source_group_by_names=None, next_token=None):
        self.name = name
        self.items = items
        self.source_group_by_names = source_group_by_names
        self.next_token = next_token

    def addItem(self, group_by_result_item):
        self.items.append(group_by_result_item)

class BaseGroupByResultItem(object):
    def __init__(self, sub_aggs, sub_group_bys):
        self.sub_aggs = sub_aggs
        self.sub_group_bys = sub_group_bys

class GroupByFieldResultItem(BaseGroupByResultItem):
    def __init__(self, key, row_count, sub_aggs, sub_group_bys):
        BaseGroupByResultItem.__init__(self, sub_aggs, sub_group_bys)

        self.key = key
        self.row_count = row_count

class GroupByRangeResultItem(BaseGroupByResultItem):
    def __init__(self, range_from, range_to, row_count, sub_aggs, sub_group_bys):
        BaseGroupByResultItem.__init__(self, sub_aggs, sub_group_bys)

        self.range_from = range_from
        self.range_to = range_to
        self.row_count = row_count

class GroupByFilterResultItem(BaseGroupByResultItem):
    def __init__(self, row_count, sub_aggs, sub_group_bys):
        BaseGroupByResultItem.__init__(self, sub_aggs, sub_group_bys)

        self.row_count = row_count

class GroupByGeoDistanceResultItem(BaseGroupByResultItem):
    def __init__(self, range_from, range_to, row_count, sub_aggs, sub_group_bys):
        BaseGroupByResultItem.__init__(self, sub_aggs, sub_group_bys)

        self.range_from = range_from
        self.range_to = range_to
        self.row_count = row_count

class GroupByHistogramResultItem(BaseGroupByResultItem):
    def __init__(self, key, value, sub_aggs, sub_group_bys):
        BaseGroupByResultItem.__init__(self, sub_aggs, sub_group_bys)

        self.key = key
        self.value = value

class GroupByComposite(BaseGroupBy):

    def __init__(self, sources, size=None, next_token=None, suggested_size=None,
                 sub_aggs=None, sub_group_bys=None, name='group_by_composite'):
        sub_aggs = [] if sub_aggs is None else sub_aggs[:]
        sub_group_bys = [] if sub_group_bys is None else sub_group_bys[:]
        BaseGroupBy.__init__(self, None, sub_aggs, sub_group_bys, name, search_pb2.GROUP_BY_COMPOSITE)

        self.sources = sources
        self.size = size
        self.next_token = next_token
        self.suggested_size = suggested_size

    def to_pb_str(self, agg_encode_func, group_by_encode_func, query_encode_func):
        proto = search_pb2.GroupByComposite()

        if self.sources is not None and isinstance(self.sources, list) and len(self.sources) > 0:
            group_by_encode_func(proto.sources, self.sources)
        else:
            raise OTSClientError('GroupByComposite: sources must be a non-empty list')

        if self.size is not None:
            if isinstance(self.size, int):
                proto.size = self.size
            else:
                raise OTSClientError('size must be integer')

        if self.next_token is not None:
            proto.next_token = self.next_token

        if self.suggested_size is not None:
            if isinstance(self.suggested_size, int):
                proto.suggested_size = self.suggested_size
            else:
                raise OTSClientError('suggested_size must be integer')

        if self.sub_aggs is not None:
            agg_encode_func(proto.sub_aggs, self.sub_aggs)

        if self.sub_group_bys is not None:
            group_by_encode_func(proto.sub_group_bys, self.sub_group_bys)

        return proto.SerializeToString()

class GroupByCompositeResultItem(BaseGroupByResultItem):
    def __init__(self, keys, row_count, sub_aggs, sub_group_bys):
        BaseGroupByResultItem.__init__(self, sub_aggs, sub_group_bys)

        self.keys = keys
        self.row_count = row_count

class DateTimeValue(object):
    def __init__(self, value, unit):
        self.value = value
        self.unit = unit

class GroupByDateHistogram(BaseGroupBy):

    def __init__(self, field_name, interval, field_range=None, missing=None, min_doc_count=None,
                 time_zone=None, group_by_sort=None, offset=None,
                 sub_aggs=None, sub_group_bys=None, name='group_by_date_histogram'):
        sub_aggs = [] if sub_aggs is None else sub_aggs[:]
        sub_group_bys = [] if sub_group_bys is None else sub_group_bys[:]
        BaseGroupBy.__init__(self, field_name, sub_aggs, sub_group_bys, name, search_pb2.GROUP_BY_DATE_HISTOGRAM)

        self.interval = interval
        self.field_range = field_range
        self.missing = missing
        self.min_doc_count = min_doc_count
        self.time_zone = time_zone
        self.group_by_sort = group_by_sort
        self.offset = offset

    def _encode_date_time_value(self, dtv):
        """将 DateTimeValue 编码为 protobuf DateTimeValue message"""
        proto = search_pb2.DateTimeValue()
        if dtv.value is not None:
            proto.value = dtv.value
        if dtv.unit is not None:
            proto.unit = self._get_enum(dtv.unit)
        return proto

    def to_pb_str(self, agg_encode_func, group_by_encode_func, query_encode_func):
        proto = search_pb2.GroupByDateHistogram()

        if self.interval is not None and isinstance(self.interval, DateTimeValue):
            proto.interval.CopyFrom(self._encode_date_time_value(self.interval))
        else:
            raise OTSClientError('GroupByDateHistogram: interval must be DateTimeValue')

        if self.field_range is not None:
            if self.field_range.min is not None:
                proto.field_range.min = bytes(PlainBufferBuilder.serialize_column_value(self.field_range.min))
            if self.field_range.max is not None:
                proto.field_range.max = bytes(PlainBufferBuilder.serialize_column_value(self.field_range.max))

        if self.missing is not None:
            proto.missing = bytes(PlainBufferBuilder.serialize_column_value(self.missing))

        if self.min_doc_count is not None:
            if isinstance(self.min_doc_count, int):
                proto.min_doc_count = self.min_doc_count
            else:
                raise OTSClientError('min_doc_count must be integer')

        if self.time_zone is not None:
            if isinstance(self.time_zone, str):
                proto.time_zone = self.time_zone
            else:
                raise OTSClientError('time_zone must be string')

        if self.group_by_sort is not None:
            if isinstance(self.group_by_sort, list):
                for sort in self.group_by_sort:
                    if isinstance(sort, GroupKeySort):
                        sorter = proto.sort.sorters.add()
                        sorter.group_key_sort.order = self._get_enum(sort.sort_order)
                    elif isinstance(sort, RowCountSort):
                        sorter = proto.sort.sorters.add()
                        sorter.row_count_sort.order = self._get_enum(sort.sort_order)
                    elif isinstance(sort, SubAggSort):
                        sorter = proto.sort.sorters.add()
                        sorter.sub_agg_sort.order = self._get_enum(sort.sort_order)
                        sorter.sub_agg_sort.sub_agg_name = sort.sub_agg_name
                    else:
                        raise OTSClientError('Invalid sort type:%s' % str(type(sort)))
            else:
                raise OTSClientError('group_by_sort must be list')

        if self.offset is not None:
            if isinstance(self.offset, DateTimeValue):
                proto.offset.CopyFrom(self._encode_date_time_value(self.offset))
            else:
                raise OTSClientError('offset must be DateTimeValue')

        BaseGroupBy._base_to_pb_str(self, proto, agg_encode_func, group_by_encode_func)
        return proto.SerializeToString()

    def _get_enum(self, e):
        return e.value if hasattr(e, 'value') else e

class GroupByDateHistogramResultItem(BaseGroupByResultItem):
    def __init__(self, timestamp, row_count, sub_aggs, sub_group_bys):
        BaseGroupByResultItem.__init__(self, sub_aggs, sub_group_bys)

        self.timestamp = timestamp
        self.row_count = row_count

class GroupByGeoGrid(BaseGroupBy):

    def __init__(self, field_name, precision, size=None,
                 sub_aggs=None, sub_group_bys=None, name='group_by_geo_grid'):
        sub_aggs = [] if sub_aggs is None else sub_aggs[:]
        sub_group_bys = [] if sub_group_bys is None else sub_group_bys[:]
        BaseGroupBy.__init__(self, field_name, sub_aggs, sub_group_bys, name, search_pb2.GROUP_BY_GEO_GRID)

        self.precision = precision
        self.size = size

    def to_pb_str(self, agg_encode_func, group_by_encode_func, query_encode_func):
        proto = search_pb2.GroupByGeoGrid()

        if self.precision is not None:
            proto.precision = self._get_enum(self.precision)
        else:
            raise OTSClientError('GroupByGeoGrid: precision must not be None')

        if self.size is not None:
            if isinstance(self.size, int):
                proto.size = self.size
            else:
                raise OTSClientError('size must be integer')

        BaseGroupBy._base_to_pb_str(self, proto, agg_encode_func, group_by_encode_func)
        return proto.SerializeToString()

    def _get_enum(self, e):
        return e.value if hasattr(e, 'value') else e

class GeoGrid(object):
    def __init__(self, top_left, bottom_right):
        self.top_left = top_left
        self.bottom_right = bottom_right

class GroupByGeoGridResultItem(BaseGroupByResultItem):
    def __init__(self, key, geo_grid, row_count, sub_aggs, sub_group_bys):
        BaseGroupByResultItem.__init__(self, sub_aggs, sub_group_bys)

        self.key = key
        self.geo_grid = geo_grid
        self.row_count = row_count
