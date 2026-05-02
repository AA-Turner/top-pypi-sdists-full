def for_each_string_array_2_string(array=[]):
    """
    遍历字符串并加上单引号
    """
    if array:
        str = None
        for tmp in array:
            if str:
                str = str + "'" + tmp + "',"
            else:
                str = "'" + tmp + "',"
        return str[0:len(str)]


def order_attribute_operation(order_attribute):
    """
    拼接order by
    """
    if order_attribute:
        order = ",".join(order_attribute)
        return "order by " + order


class ConditionOperation(object):
    singular = ["=", ">", "<", "like"]
    allCondition = ["in"]
    twoCondition = ["between"]
    special = ["timeType"]
    attribute_type_num = "num"
    attribute_type_time = "time"

    def conditionalOperation(self, typeConditions, schemas={}):
        """
        合并conditional条件
        """
        typeConditionDict = {}
        typeOrderDict = {}
        typeSpecialSql = {}
        if typeConditions:
            for typeCondition in typeConditions:
                val = None
                type = typeCondition["type"]
                schema = schemas[type]

                if "srcNodes" in typeCondition:
                    srcNodes = typeCondition["srcNodes"]
                    if srcNodes:
                        if "src" in schema:
                            if schema["src_data_type"] == self.attribute_type_num:
                                src_node = ",".join(srcNodes)
                            else:
                                src_node = for_each_string_array_2_string(srcNodes)
                            if val:
                                val = val + schema["src"] + " in(" + src_node + ") and "
                            else:
                                val = " where " + schema["src"] + " in(" + src_node + ") and "

                if "destNodes" in typeCondition:
                    destNodes = typeCondition["destNodes"]
                    if destNodes:
                        if "dst" in schema:
                            if schema["dst_data_type"] == self.attribute_type_num:
                                dest_node = ",".join(destNodes)
                            else:
                                dest_node = for_each_string_array_2_string(destNodes)
                            if val:
                                val = val + schema["dst"] + " in(" + dest_node + ") and "
                            else:
                                val = " where " + schema["dst"] + " in(" + dest_node + ") and "
                if "id" in typeCondition:
                    srcNodes = typeCondition["id"]
                    if srcNodes:
                        if "id" in schema:
                            if schema["id_data_type"] == self.attribute_type_num:
                                ids = ",".join(srcNodes)
                            else:
                                ids = for_each_string_array_2_string(srcNodes)
                            if val:
                                val = val + schema["id"] + " in(" + ids + ") and "
                            else:
                                val = " where " + schema["id"] + " in(" + ids + ") and "
                if "conditions" in typeCondition:
                    conditions = typeCondition["conditions"]
                    val_sql = val
                    val_dict = self.splice_condition(conditions, schema, val_sql)
                    if "sql" in val_dict:
                        typeSpecialSql["sql"] = val_dict["sql"]
                    val = val_dict["val"]

                if val:
                    typeConditionDict[type] = val + " 1=1"

                if "orderAttribute" in typeCondition:
                    type_order = typeCondition["orderAttribute"]
                    order_val = order_attribute_operation(type_order)
                    typeOrderDict[type] = order_val
            return typeConditionDict, typeOrderDict, typeSpecialSql

        return

    # 拼接条件
    def splice_condition(self, conditions, schema, val_sql=None):
        if conditions:
            tem_dict = {}
            if val_sql:
                val = val_sql
            else:
                val = " where "
            for condition in conditions:
                symbol = condition["symbol"]
                attribute_type = condition["type"]
                if symbol in self.singular:
                    if attribute_type == self.attribute_type_num:
                        val = val + condition["attribute"] + condition["symbol"] \
                              + condition["conditional"][0] + " and "
                    elif attribute_type == self.attribute_type_time:
                        val = val + " formatDateTime(" + condition["attribute"] + ",'%F %T') " + condition["symbol"] \
                              + " '" + condition["conditional"][0] + "' and "
                    else:
                        val = val + condition["attribute"] + condition["symbol"] \
                              + "'" + condition["conditional"][0] + "' and "

                if symbol in self.allCondition:
                    if attribute_type == self.attribute_type_num:
                        val = val + condition["attribute"] + condition["symbol"] + "(" \
                              + ",".join(condition["conditional"]) + ")" + " and "
                    else:
                        val = val + condition["attribute"] + condition["symbol"] + "(" \
                              + for_each_string_array_2_string(condition["conditional"]) + ")" + " and "
                if symbol in self.twoCondition:
                    if attribute_type == self.attribute_type_num:
                        val = val + condition["attribute"] + " between " \
                              + condition["conditional"][0] + " and " \
                              + condition["conditional"][1] + " and "
                    elif attribute_type == self.attribute_type_time:
                        val = val + " formatDateTime(" + condition["attribute"] + ",'%F %T') " + condition["symbol"] \
                              + " '" + condition["conditional"][0] + "' and "
                    else:
                        val = val + condition["attribute"] + " between '" \
                              + condition["conditional"][0] + "' and '" \
                              + condition["conditional"][1] + "' and "
                if symbol in self.special:
                    sql = self.time_line_count_sql(condition, schema, val_sql)
                    tem_dict["sql"] = sql
            tem_dict["val"] = val
            return tem_dict

    def time_line_count_sql(self, condition, schema, val_sql):
        """
        处理特殊sql的拼接
        """
        if "id" in schema and "label" in schema:
            attribute = schema["id"] + " , " + schema["label"]
        else:
            attribute = schema["src"] + " , " + schema["dst"] + " , " + schema["rank"]
        if val_sql:
            val_sql = val_sql + " 1=1 "
        else:
            val_sql = " where 1=1 "
        if condition["conditional"][0] == "year":
            sql = "select toYear(" + condition["attribute"] + ") year,count(1) count from ( select distinct " \
                  + attribute + "," + condition["attribute"] + " from " + schema["db"] + "." + schema[
                      "table"] + val_sql + " ) group by year order by year "
        elif condition["conditional"][0] == "quarter":
            sql = "select concat(toString(year),\' \',toString(quarter)) yearQuarter ,count from (select toYear(" + \
                  condition["attribute"] + ") year,toQuarter(" + condition["attribute"] \
                  + ") quarter ,count(1) count from   ( select distinct  " + attribute + "," + condition[
                      "attribute"] + " from " \
                  + schema["db"] + "." + schema["table"] \
                  + val_sql \
                  + " )  group by year,quarter order by year,quarter) "
        elif condition["conditional"][0] == "month":
            sql = "select concat(toString(year),\' \',toString(month)) yearMonth, count from ( select toYear(" + \
                  condition["attribute"] + ") year,toMonth(" + condition["attribute"] \
                  + ") month ,count(1) count from  ( select distinct " + attribute + "," + condition[
                      "attribute"] + " from " \
                  + schema["db"] + "." + schema["table"] \
                  + val_sql \
                  + " )group by year,month order by year,month)"
        elif condition["conditional"][0] == "week":
            sql = "select concat(toString(yw),\' \',toString(week)) ywWeek, count from (select toYearWeek(" + \
                  condition[
                      "attribute"] + ") yw, toDayOfWeek(" + condition["attribute"] + \
                  ") week ,count(1) count from   ( select distinct  " + attribute + "," + condition[
                      "attribute"] + " from " \
                  + schema["db"] + "." + schema["table"] \
                  + val_sql \
                  + ") group by yw,week order by yw,week )"
        elif condition["conditional"][0] == "day":
            sql = "select formatDateTime(" + condition[
                "attribute"] + ",'%F') day ,count(1) count from  ( select distinct  " \
                  + attribute + "," + condition["attribute"] + " from " \
                  + schema["db"] + "." + schema["table"] + val_sql + " ) group by day order by day"
        elif condition["conditional"][0] == "hours":
            sql = "select formatDateTime(" + condition[
                "attribute"] + ",'%F %H') h ,count(1) count from ( select distinct  " \
                  + attribute + "," + condition["attribute"] + " from " \
                  + schema["db"] + "." + schema["table"] + val_sql + " )group by h order by h"
        elif condition["conditional"][0] == "minute":
            sql = "select formatDateTime(" + condition[
                "attribute"] + ",'%F %R') m ,count(1) count from  ( select distinct  " \
                  + attribute + "," + condition["attribute"] + " from " \
                  + schema["db"] + "." + schema["table"] + val_sql + " )group by m order by m"
        else:
            sql = "select formatDateTime(" + condition[
                "attribute"] + ",'%F') day ,count(1) count from  ( select distinct  " \
                  + attribute + "," + condition["attribute"] + " from " \
                  + schema["db"] + "." + schema["table"] + val_sql + " )group by day order by day"

        return sql
