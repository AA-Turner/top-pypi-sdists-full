from typing import Optional

from tablestore.metadata import *
from tablestore.flatbuffer.dataprotocol.BytesValue import BytesValue
from tablestore.flatbuffer.dataprotocol.DataType import *
import sys
import collections
from tablestore.flatbuffer.dataprotocol.ColumnValues import *
from tablestore.flatbuffer.dataprotocol.RLEStringValues import RLEStringValues


class flat_buffer_decoder(object):
    @staticmethod
    def byte_to_str_decode(bt):
        if sys.version_info[0] == 2:
            return bt
        else:
            return bt.decode('UTF-8')

    @staticmethod
    def gen_meta_column(col_val:ColumnValues,col_tp:DataType):
        is_null_values = []
        for i in range(col_val.IsNullvaluesLength()):
            is_null_values.append(col_val.IsNullvalues(i))
        long_values = []
        for i in range(col_val.LongValuesLength()):
            long_values.append(col_val.LongValues(i))
        bool_values = []
        for i in range(col_val.BoolValuesLength()):
            bool_values.append(col_val.BoolValues(i))
        double_values = []
        for i in range(col_val.DoubleValuesLength()):
            double_values.append(col_val.DoubleValues(i))
        string_values = []
        for i in range(col_val.StringValuesLength()):
            string_values.append(flat_buffer_decoder.byte_to_str_decode(col_val.StringValues(i)))
        binary_values = []
        for i in range(col_val.BinaryValuesLength()):
            bytes_value = col_val.BinaryValues(i)
            binary_values.append(flat_buffer_decoder.gen_bytes_value(bytes_value))
        rle_string_values = col_val.RleStringValues()

        values = get_column_val_by_tp(is_null_values, long_values, bool_values, double_values, string_values, binary_values, rle_string_values, col_tp)
        if col_tp == DataType.STRING_RLE:
            values = flat_buffer_decoder.gen_rle_string_values(values)
        if len(is_null_values) != len(values):
            raise ValueError("the length of unpacked values not equal to null map")

        return [None if is_null else val for is_null, val in zip(is_null_values, values)]
    
    @staticmethod
    def gen_rle_string_values(values:RLEStringValues):
        ret = []
        for i in range(values.IndexMappingLength()):
            ret.append(values.Array(values.IndexMapping(i)).decode('UTF-8'))
        return ret

    @staticmethod
    def gen_bytes_value(bytes_value: Optional[BytesValue]):
        if bytes_value is None:
            return None
        value = []
        for i in range(bytes_value.ValueLength()):
            value.append(bytes_value.Value(i))
        return bytes(value)
        
    @staticmethod
    def format_flat_buffer_columns(columns):
        columns_meta = collections.defaultdict(list)
        for i in range(columns.ColumnsLength()):
            column = columns.Columns(i) 
            col_name = flat_buffer_decoder.byte_to_str_decode(column.ColumnName())
            col_tp = column.ColumnType()
            col_val = column.ColumnValue()
            columns_meta[col_name] = flat_buffer_decoder.gen_meta_column(col_val,col_tp)
        return columns_meta
    
    @staticmethod
    def columns_to_rows(columns_meta):
        res_list = []
        column_len = sys.maxsize
        for key in columns_meta:
            column_len = min(len(columns_meta[key]),column_len)
        for i in range(column_len):
            tup = []
            for key in columns_meta:
                tup.append((key,columns_meta[key][i]))
            row =Row(primary_key = [],attribute_columns=tup)
            res_list.append(row)
        return res_list


def get_column_val_by_tp(is_null_values, long_values, bool_values, double_values, string_values, binary_values, rle_string_values, tp):
    if tp == DataType.NONE:
        return is_null_values
    if tp == DataType.LONG:
        return long_values
    if tp == DataType.BOOLEAN:
        return bool_values
    if tp == DataType.DOUBLE:
        return double_values
    if tp == DataType.STRING:
        return string_values
    if tp == DataType.BINARY:
        return binary_values
    if tp == DataType.STRING_RLE:
        return rle_string_values
    return None