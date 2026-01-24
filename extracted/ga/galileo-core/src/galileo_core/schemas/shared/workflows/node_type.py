from enum import Enum


class NodeType(str, Enum):
    chain = "chain"
    chat = "chat"
    llm = "llm"
    retriever = "retriever"
    tool = "tool"
    agent = "agent"
    workflow = "workflow"
    trace = "trace"
    session = "session"
