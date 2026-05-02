import requests
import json

if __name__ == '__main__':

# graph deletion
    url_graph_deletion = "http://p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/graph-deletion"
    data_graph_deletion = json.dumps({
        "graph_name": "taobao_v1"
    })
    response = requests.delete(url=url_graph_deletion, data=data_graph_deletion)
    print(response.text)


# match edge
    url_edges = "http://p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/edges"
    data_edges = json.dumps({
        "graph_name": "taobao_v1",
        "edge_name": "user_adgroup",
        "edge_con_list": [
            "record_date='2017-05-12'",
            "record_time>'2017-05-12 23:30:00'",
            "pid='430548_1007'"],
        "target_field_list": ["record_time"]
    })
    response = requests.get(url=url_edges, data=data_edges)
    print(response.text)


# match vertices
    url_vertices = "http://p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/vertices"
    data_vertices = json.dumps({
        "graph_name": "taobao_v1",
        "vertex_name": "user",
        "vertex_con_list": [
            "final_gender_code='2'",
            "age_level='6'",
            "pvalue_level='2'",
            "shopping_level='3'",
            "occupation='0'"
        ],
        "target_field_list": [
            "new_user_class_level",
            "record_date"
        ]
    })
    response = requests.get(url=url_vertices, data=data_vertices)
    print(response.text)


# multi-hop
    url_multi_hop = "http://p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/multi-hop"
    data_multi_hop = json.dumps({
        "graph_name": "taobao_v1",
        "step": 2,
        "start_vertex_list": ["255837", "255813"],
        "edge_name_list": [
            "user_adgroup",
            "adgroup_customer"
        ],
        "direction": "backward",
        "edge_con_list_list": [
            [],
            []
        ],
        "target_field_list": [
            "record_time"
        ],
        "only_last_step": False,
        "plus_last_vertexes": False
    })
    response = requests.get(url=url_multi_hop, data=data_multi_hop)
    print(response.text)


# one-hop
    url_one_hop = "http://p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/one-hop"
    data_one_hop = json.dumps({
        "start_vertex_list": [
            "1000007",
            "100000",
            "843732"
        ],
        "edge_name_list": [
            "userid_adgroup",
            "adgroup_customer"
        ],
        "graph_name": "taobao_v1",
        "direction": "forward",
        "edge_con_list_list": [
            [
                "record_date='2017-5-13'"
            ],
            [
                "record_date='2017-5-9'"
            ]
        ],
        "target_field_list": [
            "record_time"
        ]
    })
    response = requests.get(url=url_one_hop, data=data_one_hop)
    print(response.text)


# match multi_hop_common_vertices
    url_multi_hop_common_vertices = "http://p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/multi-hop-common-vertices"
    data_multi_hop_common_vertices = json.dumps({
        "step": 1,
        "start_vertex_list": [
            "162433",
            "164028",
            "165628"
        ],
        "edge_name_list": [
            "userid_adgroup",
            "adgroup_customer"
        ],
        "graph_name": "taobao_v1",
        "direction": "forward",
        "edge_con_list_list": [[], []]
    })
    response = requests.get(url=url_multi_hop_common_vertices, data=data_multi_hop_common_vertices)
    print(response.text)


# path
    url_path = "http://p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/path"
    data_path= json.dumps({
        "graph_name": "taobao_v1",
        "start_vertex_list": ["596729","326033","596729"],
        "end_vertex_list": ["255837","255813"],
        "edge_name_list": ["user_adgroup","adgroup_customer"],
        "edge_con_list_list": [[],[]],
        "target_field_list": ["record_time"],
        "step_limit":2
    })
    response = requests.get(url=url_path, data=data_path)
    print(response.text)


# graph registration
    url_graph_registration = "http://p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/graph-registration"
    data_graph_registration = json.dumps({
        "graph_name": "taobao_v1",
        "graph_cfg": {"edges":{"adgroup_customer":{"db":"taobao","table":"adgroup_customerid_edge","src":"adgroup_id","dst":"customer_id","rank":"record_time","fields":["record_date","record_time"]      },"user_adgroup":{"db":"taobao","table":"userid_adgroup_edge","src":"user_id","dst":"adgroup_id","rank":"record_time","fields":["record_date","record_time","pid"]      }},"vertexes":{"user":{"db":"taobao","table":"user_profile","id":"user_id","fields":["record_date", "cms_segid", "cms_group_id", "final_gender_code", "age_level", "pvalue_level", "shopping_level", "occupation", "new_user_class_level"]},"adgroup":{"db":"taobao","table":"ad_feature","id":"adgroup_id","fields":["record_date","cate_id","campaign_id","brand","price"]}}}
    })
    response = requests.post(url=url_graph_registration, data=data_graph_registration)
    print(response.text)


# graph show
    url_graph_show = "http://p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/graph-show"
    data_graph_show = json.dumps({})
    response = requests.get(url=url_graph_show, data=data_graph_show)
    print(response.text)


# graph summary
    url_graph_summary = "http://p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/graph-summary/taobao_v1"
    # data_graph_summary = json.dumps({
    #     "graph_name": "livejournal_v1"
    # })
    response = requests.get(url=url_graph_summary)
    print(response.text)


# graph description
    url_graph_description = "http://p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/graph-description/taobao_v1"
    # data_graph_description = json.dumps({
    #     "graph_name": "livejournal_v1"
    # })
    response = requests.get(url=url_graph_description)
    print(response.text)


# subgraph creation
    url_subgraph_creation = "p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/subgraph-creation"
    data_subgraph_creation = json.dumps({
        "graph_name": "taobao_v1",
        "subgraph_name":"taobao_v1_sub"
    })
    response = requests.get(url=data_subgraph_creation)
    print(response.text)

# subgraph destruction
    url_subgraph_destruction = "p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/subgraph-destruction"
    data_subgraph_destruction = json.dumps({
        "graph_name": "taobao_v1",
        "subgraph_name":"taobao_v1_sub"
    })
    response = requests.get(url=data_subgraph_destruction)
    print(response.text)

# subgraph update multi hop
    url_subgraph_update_multi_hop = "p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/subgraph-update-multi-hop"
    data_subgraph_update_multi_hop = json.dumps({
            "graph_name": "taobao_v1",
            "subgraph_name":"taobao_v1_sub",
            "step": 2,
            "start_vertex_list": ["255837", "255813"],
            "edge_name_list": [
                "user_adgroup",
                "adgroup_customer"
            ],
            "direction": "backward",
            "edge_con_list_list": [
                [],
                []
            ]
    })
    response = requests.get(url=data_subgraph_update_multi_hop)
    print(response.text)

# subgraph update path
    url_subgraph_update_path = "p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/subgraph-update-path"
    data_subgraph_update_path = json.dumps({
        "graph_name": "taobao_v1",
        "subgraph_name":"taobao_v1_sub",
        "start_vertex_list": ["596729", "326033", "596729"],
        "end_vertex_list": ["255837", "255813"],
        "edge_name_list": ["user_adgroup", "adgroup_customer"],
        "edge_con_list_list": [[], []],
        "step_limit": 2
    })
    response = requests.get(url=data_subgraph_update_path)
    print(response.text)


# subgraph update edge
    url_subgraph_update_edge = "p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/subgraph-update-edge"
    data_subgraph_update_edge = json.dumps({
        "graph_name": "taobao_v1",
        "subgraph_name": "taobao_v1_sub",
        "edge_name": "user_adgroup",
        "edge_con_list": [
            "record_date='2017-05-12'",
            "record_time>'2017-05-12 23:30:00'",
            "pid='430548_1007'"
        ]
    })
    response = requests.get(url=data_subgraph_update_edge)
    print(response.text)
