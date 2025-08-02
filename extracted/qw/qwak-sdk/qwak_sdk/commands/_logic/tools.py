from google.protobuf.json_format import MessageToJson


def list_of_messages_to_json_str(list_of_proto_msgs) -> str:
    json_msgs = [MessageToJson(proto_msg) for proto_msg in list_of_proto_msgs]
    return "[" + ",".join(json_msgs) + "]"
