import requests
import json

if __name__ == '__main__':

# graph deletion
    url_graph_deletion = "http://p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/graph-deletion"
    data_graph_deletion = json.dumps({
        "graph_name": "twitter_v1"
    })
    response = requests.delete(url=url_graph_deletion, data=data_graph_deletion)
    print(response.text)


# match edge
    url_edges = "http://p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/edges"
    data_edges = json.dumps({
        "graph_name": "twitter_v1",
        "edge_name": "follow",
        "edge_con_list": ["follow_date>'2010-12-31'"],
        "target_field_list": ["follow_date"],
        "data_type": "df"
    })
    response = requests.get(url=url_edges, data=data_edges)
    print(response.text)


# multi-hop
    url_multi_hop = "http://p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/multi-hop"

    data_multi_hop = json.dumps({
        "graph_name": "twitter_v1",
        "step": 1,
        "start_vertex_list": ['10000082','10000162'],
        "edge_name_list": ["follow"],
        "direction": "forward",
        "edge_con_list_list": [["follow_date>'2010-06-30'"]],
        "target_field_list": ["follow_date"],
        "only_last_step": False,
        "plus_last_vertexes": False
    })
    response = requests.get(url=url_multi_hop, data=data_multi_hop)
    print(response.text)


# one-hop
    url_one_hop = "http://p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/one-hop"
    data_one_hop = json.dumps({
        "graph_name": "twitter_v1",
        "step": 1,
        "start_vertex_list": ['10000082','10000162'],
        "edge_name_list": ["follow"],
        "direction": "forward",
        "edge_con_list_list": [["follow_date>'2010-06-30'"]],
        "target_field_list": ["follow_date"],
        "only_last_step": False,
        "plus_last_vertexes": False
    })
    response = requests.get(url=url_one_hop, data=data_one_hop)
    print(response.text)


# match multi_hop_common_vertices
    url_multi_hop_common_vertices = "http://p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/multi-hop-common-vertices"

    data_multi_hop_common_vertices = json.dumps({
        "step": 1,
        "start_vertex_list": [
            '10000082',
            '10000162'
        ],
        "edge_name_list": [
            "follow"
        ],
        "graph_name": "twitter_v1",
        "direction": "forward",
        "edge_con_list_list": [
            ["follow_date>'2010-06-30'"]
        ]
    })
    response = requests.get(url=url_multi_hop_common_vertices, data=data_multi_hop_common_vertices)
    print(response.text)


# path
    url_path = "http://p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/path"
    data_path = json.dumps({
        "graph_name": "twitter_v1",
        "start_vertex_list": [
            '10000082',
            '10000162'
        ],
        "end_vertex_list": ['49265462', '9170712', '42506240', '28088190'],
        "edge_name_list": ["follow"],
        "edge_con_list_list": [["follow_date>'2010-06-30'"]],
        "target_field_list": ["follow_date"],
        "step_limit": 1
    })
    response = requests.get(url=url_path, data=data_path)
    print(response.text)


# graph registration
    url_graph_registration = "http://p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/graph-registration"
    data_graph_registration = json.dumps({
        "graph_name": "twitter_v1",
        "graph_cfg": "{\"edges\":{\"follow\":{\"db\":\"twitter_v1\",\"table\":\"follow\",\"src\":\"followee_id\",\"dst\":\"follower_id\",\"fields\":[\"follow_date\"]}},\"vertexes\":{}}"
    })
    response = requests.post(url=url_graph_registration, data=data_graph_registration)
    print(response.text)


# graph show
    url_graph_show = "http://p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/graph-show"
    data_graph_show = json.dumps({})
    response = requests.get(url=url_graph_show, data=data_graph_show)
    print(response.text)


# graph summary
    url_graph_summary = "http://p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/graph-summary/twitter_v1"
    # data_graph_summary = json.dumps({
    #     "graph_name": "livejournal_v1"
    # })
    response = requests.get(url=url_graph_summary)
    print(response.text)


# graph description
    url_graph_description = "http://p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/graph-description/twitter_v1"
    # data_graph_description = json.dumps({
    #     "graph_name": "livejournal_v1"
    # })
    response = requests.get(url=url_graph_description)
    print(response.text)


# subgraph creation
    url_subgraph_creation = "p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/subgraph-creation"
    data_subgraph_creation = json.dumps({
        "graph_name": "twitter_v1",
        "subgraph_name": "twitter_v1_sub"
    })
    response = requests.get(url=data_subgraph_creation)
    print(response.text)


# subgraph destruction
    url_subgraph_destruction = "p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/subgraph-destruction"
    data_subgraph_destruction = json.dumps({
        "graph_name": "twitter_v1",
        "subgraph_name":"twitter_v1_sub"
    })
    response = requests.get(url=data_subgraph_destruction)
    print(response.text)

# subgraph update multi hop
    url_subgraph_update_multi_hop = "p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/subgraph-update-multi-hop"
    data_subgraph_update_multi_hop = json.dumps({
            "graph_name": "twitter_v1",
            "subgraph_name":"twitter_v1_sub",
            "step": 1,
            "start_vertex_list": ['10000082','10000162'],
            "edge_name_list": ["follow"],
            "direction": "forward",
            "edge_con_list_list": [["follow_date>'2010-06-30'"]]
    })
    response = requests.get(url=data_subgraph_update_multi_hop)
    print(response.text)

# subgraph update path
    url_subgraph_update_path = "p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/subgraph-update-path"
    data_subgraph_update_path = json.dumps({
            "graph_name": "twitter_v1",
            "subgraph_name":"twitter_v1_sub",
            "start_vertex_list": [
                '10000082',
                '10000162'
            ],
            "end_vertex_list": ['49265462', '9170712', '42506240', '28088190'],
            "edge_name_list": ["follow"],
            "edge_con_list_list": [["follow_date>'2010-06-30'"]],
            "step_limit": 1
    })
    response = requests.get(url=data_subgraph_update_path)
    print(response.text)


# subgraph update edge
    url_subgraph_update_edge = "p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/subgraph-update-edge"
    data_subgraph_update_edge = json.dumps({
            "graph_name": "twitter_v1",
            "subgraph_name":"twitter_v1_sub",
            "edge_name": "follow",
            "edge_con_list": ["follow_date>'2010-12-31'"],
            "target_field_list": ["follow_date"],
            "data_type": "df"
    })
    response = requests.get(url=data_subgraph_update_edge)
    print(response.text)
