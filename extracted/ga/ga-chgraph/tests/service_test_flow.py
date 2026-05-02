import requests
import json

if __name__ == '__main__':


# graph deletion
    url_graph_deletion = "http://p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/graph-deletion"
    data_graph_deletion = json.dumps({
        "graph_name": "cyber3"
    })
    response = requests.delete(url=url_graph_deletion, data=data_graph_deletion)
    print(response.text)


# match edge
    url_edges = "http://p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/edges"
    data_edges = json.dumps({
        "edge_name": "tcpflow",
        "graph_name": "cyber3",
        "edge_con_list": [
            "downlink_length>100000000"
        ],
        "target_field_list": [
            "record_time",
            "downlink_length"
        ]
    })
    response = requests.get(url=url_edges, data=data_edges)
    print(response.text)


# match vertices
#     url_edges = "http://p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/vertices"
#     data_edges = json.dumps(
#       {
#
#       }
#     )
#     response = requests.get(url=url_edges, data=data_edges)
#     print(response.text)


# multi-hop
    url_multi_hop = "http://p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/multi-hop"
    data_multi_hop = json.dumps({
        "step": 2,
        "start_vertex_list": [
            "10.73.28.115",
            "10.78.55.20"
        ],
        "edge_name_list": [
            "tcpflow",
            "flow"
        ],
        "graph_name": "cyber3",
        "direction": "forward",
        "edge_con_list_list": [
            [
                "downlink_length>10000",
                "protocol='http'"
            ],
            [
                "record_date='2019-04-15'"
            ]
        ],
        "target_field_list": [
            "record_time"
        ],
        "only_last_step": True,
        "plus_last_vertexes": True
    })
    response = requests.get(url=url_multi_hop, data=data_multi_hop)
    print(response.text)


# match one-hop
    url_one_hop = "http://p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/one-hop"
    data_one_hop = json.dumps({
        "start_vertex_list": [
            "10.73.28.115",
            "10.78.55.20"
        ],
        "edge_name_list": [
            "tcpflow",
            "flow"
        ],
        "graph_name": "cyber3",
        "direction": "forward",
        "edge_con_list_list": [
            [
                "downlink_length>1000",
                "protocol='http'"
            ],
            [
                "record_date='2019-04-15'"
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
        "step": 2,
        "start_vertex_list": [
            "10.73.28.115",
            "10.78.55.20"
        ],
        "edge_name_list": [
            "tcpflow",
            "flow"
        ],
        "graph_name": "cyber3",
        "direction": "forward",
        "edge_con_list_list": [
            [
                "protocol='http'"
            ],
            [
                "record_date='2019-04-15'"
            ]
        ],
        "only_last_step":False
    })
    response = requests.get(url=url_multi_hop_common_vertices, data=data_multi_hop_common_vertices)
    print(response.text)


# path
    url_path = "http://p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/path"
    data_path= json.dumps({
        "step_limit": 2,
        "start_vertex_list": [
            "10.73.28.115"
        ],
        "end_vertex_list": [
            "106.38.199.41",
            "10.59.81.218"
  ],
        "edge_name_list": [
            "tcpflow",
            "flow"
        ],
        "graph_name": "cyber3",
        "edge_con_list_list": [
            [
                "downlink_length>10000",
                "protocol='http'"
            ],
            [
                "record_date='2019-04-15'"
            ]
        ],
        "target_field_list": [
            "record_time"
        ]
    })
    response = requests.get(url=url_path, data=data_path)
    print(response.text)


# graph registration
    url_graph_registration = "http://p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/graph-registration"
    data_graph_registration = json.dumps({
        "graph_name": "cyber_10",
        "graph_cfg": "{\"edges\":{\"tcpflow\":{\"db\":\"graph\",\"table\":\"tcpflow\",\"src\":\"source_ip\",\"dst\":\"destination_ip\",\"rank\":\"record_time\",\"fields\":[\"record_date\",\"record_time\",\"protocol\",\"destination_port\",\"uplink_length\",\"downlink_length\"] },\"flow\":{\"db\":\"graph\",\"table\":\"flow\",\"src\":\"source_ip\",\"dst\":\"destination_ip\", \"rank\":\"record_time\",\"fields\":[\"record_date\",\"record_time\",\"destination_port\",\"uri\"]}},\"vertexes\":{}}"
    })
    response = requests.post(url=url_graph_registration, data=data_graph_registration)
    print(response.text)


# graph show
    url_graph_show = "http://p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/graph-show"
    data_graph_show = json.dumps({})
    response = requests.get(url=url_graph_show, data=data_graph_show)
    print(response.text)


# graph summary
    url_graph_summary = "http://p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/graph-summary/cyber3"
    # data_graph_summary = json.dumps({
    #     "graph_name": "livejournal_v1"
    # })
    response = requests.get(url=url_graph_summary)
    print(response.text)


# graph description
    url_graph_description = "http://p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/graph-description/cyber3"
    # data_graph_description = json.dumps({
    #     "graph_name": "livejournal_v1"
    # })
    response = requests.get(url=url_graph_description)
    print(response.text)


# subgraph creation
    url_subgraph_creation = "p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/subgraph-creation"
    data_subgraph_creation = json.dumps({
        "graph_name": "cyber_10",
        "subgraph_name":"cyber_10_sub1"
    })
    response = requests.get(url=data_subgraph_creation)
    print(response.text)

# subgraph destruction
    url_subgraph_destruction = "p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/subgraph-destruction"
    data_subgraph_destruction = json.dumps({
        "graph_name": "cyber_10",
        "subgraph_name":"cyber_10_sub1"
    })
    response = requests.get(url=data_subgraph_destruction)
    print(response.text)

# subgraph update multi hop
    url_subgraph_update_multi_hop = "p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/subgraph-update-multi-hop"
    data_subgraph_update_multi_hop = json.dumps({
        "step": 2,
        "start_vertex_list": [
            "10.73.28.115",
            "10.78.55.20"
        ],
        "edge_name_list": [
            "tcpflow",
            "flow"
        ],
        "graph_name": "cyber_10",
        "subgraph_name": "cyber_10_sub1",
        "direction": "forward",
        "edge_con_list_list": [
            [
                "downlink_length>10000",
                "protocol='http'"
            ],
            [
                "record_date='2019-04-15'"
            ]
        ]
    })
    response = requests.get(url=data_subgraph_update_multi_hop)
    print(response.text)

# subgraph update path
    url_subgraph_update_path = "p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/subgraph-update-path"
    data_subgraph_update_path = json.dumps({
            "step_limit": 2,
            "start_vertex_list": [
                "10.73.28.115"
            ],
            "end_vertex_list": [
                "106.38.199.41",
                "10.59.81.218"
            ],
            "edge_name_list": [
                "tcpflow",
                "flow"
            ],
            "graph_name": "cyber_10",
            "subgraph_name": "cyber_10_sub1",
            "edge_con_list_list": [
                [
                    "downlink_length>10000",
                    "protocol='http'"
                ],
                [
                    "record_date='2019-04-15'"
                ]
            ]
    })
    response = requests.get(url=data_subgraph_update_path)
    print(response.text)


# subgraph update edge
    url_subgraph_update_edge = "p47708v.hulk.shbt.qihoo.net:10010/graph-db/api/v1/subgraph-update-edge"
    data_subgraph_update_edge = json.dumps({
        "edge_name": "tcpflow",
        "graph_name": "cyber_10",
        "subgraph_name": "cyber_10_sub1",
        "edge_con_list": [
            "downlink_length>100000000"
        ]
    })
    response = requests.get(url=data_subgraph_update_edge)
    print(response.text)

