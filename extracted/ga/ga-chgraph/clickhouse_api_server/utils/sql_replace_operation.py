import re
"""
替换sql
"""


class SqlReplaceHandler(object):
    def __init__(self, is_cluster=False):
        self.is_cluster = is_cluster

    @staticmethod
    def replace_in_with_global_in(origin_sql):
        """
        sql中的关键字必须小写
        """
        pattern = r" in \( *select +"
        return re.sub(pattern, " global in (select ", origin_sql)

    @staticmethod
    def replace_join_with_global_join(origin_sql):
        patterns = [
            (r"( inner join \( *select )|( join \( *select )", " global join (select "),

            (r"( left outer join \( *select )|( left join \( *select )|( left outer global join \( *select )|"
             r"( left global join \( *select )",  " global left join (select "),

            (r"( right outer join \( *select )|( right join \( *select )|( right outer global join \( *select )|"
             r"( right global join \( *select )", " global right join (select "),

            (r"( cross join \( *select )|( cross global join \( *select )", " global cross join (select "),

        ]

        for pattern, repl in patterns:
            origin_sql = re.sub(pattern, repl, origin_sql)

        return origin_sql

    def deal_sql(self, origin_sql):
        if not self.is_cluster:
            return origin_sql

        if re.search(r" in \( *select +", origin_sql):
            sql = self.replace_in_with_global_in(origin_sql)
        else:
            sql = origin_sql

        if "join" in sql:
            sql = self.replace_join_with_global_join(sql)
        else:
            sql = origin_sql
        return sql


if __name__ == "__main__":
    handler = SqlReplaceHandler(True)

    sql_1 = "insert into default.user_record (*) select * from login_record\
                  where user_id in ( select user_id from login_record where user_id>8)"
    new_sql = handler.deal_sql(sql_1)
    print("new sql: ", new_sql)

    sql_2 = "insert into default.user_record (*) select * from login_record\
                      where user_id in ('select', 'a', 'b')"
    new_sql = handler.deal_sql(sql_2)
    print("new sql: ", new_sql)

    sql_3 = "select * from default.login_record l inner join (select * from default.user_record) u on l.user_id=u.user_id;"
    sql_3 = handler.deal_sql(sql_3)
    print("sql3: {}\n".format(sql_3))

    sql_4 = "select * from default.login_record l left outer join (select * from default.user_record) u on l.user_id=u.user_id;"
    sql_4 = handler.deal_sql(sql_4)
    print("sql4: {}\n".format(sql_4))

    sql_5 = "select l.* from default.default_metamembers as l join (select member_id id from (SELECT * FROM default_mergeedge limit 30  )) as r on l.member_id=r.id"
    sql_5 = handler.deal_sql(sql_5)
    print("sql5: {}\n".format(sql_5))
