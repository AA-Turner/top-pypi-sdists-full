
def deal_query_result(data_type, client, sql):
    if data_type == "list":
        res = client.execute(sql)
    elif data_type == "df":
        res = {}
        result = client.query_dataframe(sql)
        res['schema'] = result.columns.values.tolist()
        res['detail'] = result.values.tolist()
    else:
        res = None

    return res


def deal_query_result_sample(data_type, client, sql):
    if data_type == "list":
        res = client.execute(sql)
    elif data_type == "df":
        res = client.query_dataframe(sql)
    else:
        res = None

    return res


def deal_query_result_sample_plus(data_type, client, sql):
    if data_type == "list":
        res = client.execute(sql)
    elif data_type == "df":
        res = client.query_dataframe(sql).values.tolist()
    else:
        res = None

    return res


def deal_query_result_with_paging(data_type, client, sql, page, page_size, count):
    if data_type == "list":
        res = client.execute(sql)
    elif data_type == "df":
        res = {}
        result = client.query_dataframe(sql)
        res['schema'] = result.columns.values.tolist()
        res['detail'] = result.values.tolist()
        res['page'] = page
        res['page_size'] = page_size
        res['count'] = count
    else:
        res = None

    return res
