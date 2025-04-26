from typing import Optional, Literal, Any

from openapi_client import V1WorkflowNodeStruct, V1WorkflowNodeInlineCode, V1BaseWorkflowNode, V1WorkflowNodeLLMQuery, \
    V1WorkflowNodeLLMQueryRequest, V1WorkflowNodeVectorSearch, V1WorkflowNodeVectorSearchRequest, V1SingleWorkflowEdge, \
    V1WorkflowNodeInput, V1SingleLLMQueryMessage, V1SingleWorkflowNodeOutput, V1WorkflowRevisionInput, \
    V1VariableValueInput, V1SingleWorkflowEdgeInput
from vessl.llm import connection


class WorkflowEdge(object):
    when: Optional[str]
    otherwise: Optional[bool]
    next_node: str

    def __init__(self, when: Optional[str], otherwise: Optional[bool], next_node: str):
        self.when = when
        self.otherwise = otherwise
        self.next_node = next_node

    @classmethod
    def from_config(cls, edge: V1SingleWorkflowEdge):
        return cls(edge.when, edge.otherwise, edge.next_node)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]):
        return cls(payload.get("when"), payload.get("otherwise"), payload.get("next_node"))

    def to_v1_single_workflow_edge_input(self) -> V1SingleWorkflowEdgeInput:
        return V1SingleWorkflowEdgeInput(
            when=self.when,
            otherwise=self.otherwise,
            next_node=self.next_node
        )


class SingleNodeOutput(object):
    text: Optional[str]
    expr: Optional[str]

    def __init__(self, text: Optional[str], expr: Optional[str]):
        self.text = text
        self.expr = expr

    @classmethod
    def from_config(cls, output: V1SingleWorkflowNodeOutput):
        return cls(output.text, output.expr)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]):
        return cls(payload.get("text"), payload.get("expr"))

    def to_v1_single_workflow_node_output(self) -> V1SingleWorkflowNodeOutput:
        return V1SingleWorkflowNodeOutput(
            text=self.text,
            expr=self.expr
        )


class BaseWorkflowNode(object):
    title: str
    outputs: dict[str, SingleNodeOutput]

    def __init__(self, title: str, outputs: dict[str, SingleNodeOutput]):
        self.title = title
        self.outputs = outputs

    def to_v1_base_workflow_node(self) -> V1BaseWorkflowNode:
        return V1BaseWorkflowNode(title=self.title, outputs={
            k: v.to_v1_single_workflow_node_output() for k, v in self.outputs.items()
        })


class WorkflowNodeInlineCode(BaseWorkflowNode):
    code: str

    def __init__(self, code: str, base_config: Optional[V1BaseWorkflowNode] = None,
                 base_dict: Optional[dict[str, Any]] = None):
        if base_config is not None:
            if base_config.outputs is not None:
                outputs = {k: SingleNodeOutput.from_config(v) for k, v in base_config.outputs.items()}
            else:
                outputs = dict()
            super().__init__(base_config.title, outputs)
        else:
            outputs = {k: SingleNodeOutput.from_dict(v) for k, v in base_dict.get("outputs", {}).items()}
            super().__init__(base_dict.get("title"), outputs)
        self.code = code

    @classmethod
    def from_config(cls, inline_code: V1WorkflowNodeInlineCode):
        return cls(code=inline_code.code, base_config=inline_code.base_workflow_node)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]):
        return cls(code=payload.get("code"), base_dict=payload.get("base_workflow_node", {}))

    def to_v1_workflow_node_inline_code(self) -> V1WorkflowNodeInlineCode:
        return V1WorkflowNodeInlineCode(
            base_workflow_node=self.to_v1_base_workflow_node(),
            code=self.code
        )


class LLMQueryMessage(object):
    RoleSystem = "system"
    RoleUser = "user"
    RoleAgent = "agent"
    RoleType = Literal["system", "user", "agent"]
    role: RoleType
    content: str

    def __init__(self, role: RoleType, content: str):
        self.role = role
        self.content = content

    @classmethod
    def from_config(cls, message: V1SingleLLMQueryMessage):
        role: Literal["system", "user", "agent"] = "system"
        if message.role == "user":
            role = "user"
        elif message.role == "agent":
            role = "agent"
        return cls(role, message.content)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]):
        return cls(payload.get("role"), payload.get("content"))


class LLMQueryRequest(object):
    messages: list[LLMQueryMessage]
    payload: dict[str, Any]

    def __init__(self, messages: list[LLMQueryMessage], payload: dict[str, Any]):
        self.messages = messages
        self.payload = payload

    @classmethod
    def from_config(cls, request: V1WorkflowNodeLLMQueryRequest):
        messages = [LLMQueryMessage.from_config(message) for message in request.messages]
        return cls(messages, request.payload)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]):
        messages = [LLMQueryMessage.from_dict(message) for message in payload.get("messages", [])]
        return cls(messages, payload.get("payload"))


class WorkflowNodeLLMQuery(BaseWorkflowNode):
    request: LLMQueryRequest
    llm_model: connection.ModelConnection
    model_connection_name: str

    def __init__(self, request: LLMQueryRequest, model_connection_name: str,
                 llm_model: Optional[connection.ModelConnection] = None,
                 base_config: Optional[V1BaseWorkflowNode] = None, base_dict: Optional[dict[str, Any]] = None):
        if base_config is not None:
            if base_config.outputs is not None:
                outputs = {k: SingleNodeOutput.from_config(v) for k, v in base_config.outputs.items()}
            else:
                outputs = dict()
            super().__init__(base_config.title, outputs)
        else:
            outputs = {k: SingleNodeOutput.from_dict(v) for k, v in base_dict.get("outputs", {}).items()}
            super().__init__(base_dict.get("title"), outputs)

        self.request = request
        self.llm_model = llm_model
        self.model_connection_name = model_connection_name

    @classmethod
    def from_config(cls, llm_query: V1WorkflowNodeLLMQuery, llm_model: connection.ModelConnection):
        base_workflow_node: V1BaseWorkflowNode = llm_query.base_workflow_node
        request = LLMQueryRequest.from_config(llm_query.request)
        model_connection_name = llm_query.model_connection_name
        return cls(request, model_connection_name, llm_model=llm_model, base_config=base_workflow_node)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]):
        # only called when building input from any, thus no llm_model is passed
        request = LLMQueryRequest.from_dict(payload.get("request", {}))
        model_connection_name = payload.get("model_connection_name")
        return cls(request, model_connection_name, base_dict=payload.get("base_workflow_node", {}))

    def to_v1_workflow_node_llm_query(self) -> V1WorkflowNodeLLMQuery:
        messages = [
            V1SingleLLMQueryMessage(role=message.role, content=message.content) for message in self.request.messages
        ]
        return V1WorkflowNodeLLMQuery(
            base_workflow_node=self.to_v1_base_workflow_node(),
            request=V1WorkflowNodeLLMQueryRequest(
                messages=messages,
                payload=self.request.payload,
            ),
            model_connection_name=self.model_connection_name
        )


class VectorSearchRequest(object):
    input: str
    payload: dict[str, Any]

    def __init__(self, input_str: str, payload: dict[str, Any]):
        self.input = input_str
        self.payload = payload

    @classmethod
    def from_config(cls, request: V1WorkflowNodeVectorSearchRequest):
        return cls(request.input, request.payload)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]):
        return cls(payload.get("input"), payload.get("payload"))


class WorkflowNodeVectorSearch(BaseWorkflowNode):
    request: VectorSearchRequest
    knowledge_name: str
    embedding_model: Optional[connection.ModelConnection]
    vector_db: Optional[connection.VectorDBConnection]
    permission: Optional[connection.PermissionConfig]

    def __init__(self, request: VectorSearchRequest, knowledge_name: str,
                 embedding_model: Optional[connection.ModelConnection] = None,
                 vector_db: Optional[connection.VectorDBConnection] = None,
                 permission: Optional[connection.PermissionConfig] = None,
                 base_config: Optional[V1BaseWorkflowNode] = None, base_dict: Optional[dict[str, Any]] = None):
        if base_config is not None:
            if base_config.outputs is not None:
                outputs = {k: SingleNodeOutput.from_config(v) for k, v in base_config.outputs.items()}
            else:
                outputs = dict()
            super().__init__(base_config.title, outputs)
        else:
            outputs = {k: SingleNodeOutput.from_dict(v) for k, v in base_dict.get("outputs", {}).items()}
            super().__init__(base_dict.get("title"), outputs)

        self.request = request
        self.knowledge_name = knowledge_name
        self.embedding_model = embedding_model
        self.vector_db = vector_db
        self.permission = permission

    @classmethod
    def from_config(cls, vector_search: V1WorkflowNodeVectorSearch, embedding_model: connection.ModelConnection,
                    vector_db: connection.VectorDBConnection, permission: connection.PermissionConfig):
        knowledge_name = vector_search.knowledge_name
        base_workflow_node: V1BaseWorkflowNode = vector_search.base_workflow_node
        request = VectorSearchRequest.from_config(vector_search.request)
        return cls(request, knowledge_name, embedding_model=embedding_model, vector_db=vector_db,
                   permission=permission, base_config=base_workflow_node)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]):
        # only called when building input from any, thus no embedding_model, vector_db, permission is passed
        request = VectorSearchRequest.from_dict(payload.get("request", {}))
        knowledge_name = payload.get("knowledge_name")
        return cls(request, knowledge_name, base_dict=payload.get("base_workflow_node", {}))

    def to_v1_workflow_node_vector_search(self) -> V1WorkflowNodeVectorSearch:
        return V1WorkflowNodeVectorSearch(
            base_workflow_node=self.to_v1_base_workflow_node(),
            request=V1WorkflowNodeVectorSearchRequest(input=self.request.input, payload=self.request.payload),
            knowledge_name=self.knowledge_name,
        )


class WorkflowNode(object):
    NodeKind = Literal[
        "workflowv1/InlineCode", "workflowv1/LLMQuery", "workflowv1/VectorSearch", "workflowv1/InvokeTool"]
    NodeInlineCode: NodeKind = "workflowv1/InlineCode"
    NodeLLMQuery: NodeKind = "workflowv1/LLMQuery"
    NodeVectorSearch: NodeKind = "workflowv1/VectorSearch"
    NodeInvokeTool: NodeKind = "workflowv1/InvokeTool"
    kind: NodeKind
    vector_search: Optional[WorkflowNodeVectorSearch]
    llm_query: Optional[WorkflowNodeLLMQuery]
    inline_code: Optional[WorkflowNodeInlineCode]

    def __init__(self, kind: NodeKind,
                 vector_search: Optional[WorkflowNodeVectorSearch] = None,
                 llm_query: Optional[WorkflowNodeLLMQuery] = None,
                 inline_code: Optional[WorkflowNodeInlineCode] = None):
        self.kind = kind
        self.vector_search = vector_search
        self.llm_query = llm_query
        self.inline_code = inline_code

    @classmethod
    def from_config(cls, node: V1WorkflowNodeStruct, model_connection: Optional[connection.ModelConnection],
                    vector_db: Optional[connection.VectorDBConnection],
                    permission: Optional[connection.PermissionConfig]):

        if node.kind == cls.NodeInlineCode:
            return cls(kind=cls.NodeInlineCode, inline_code=WorkflowNodeInlineCode.from_config(node.inline_code))
        elif node.kind == cls.NodeLLMQuery:
            return cls(kind=cls.NodeLLMQuery, llm_query=WorkflowNodeLLMQuery.from_config(
                node.llm_query, model_connection,
            ))
        elif node.kind == cls.NodeVectorSearch:
            return cls(kind=cls.NodeVectorSearch, vector_search=WorkflowNodeVectorSearch.from_config(
                node.vector_search, model_connection, vector_db, permission,
            ))

    @classmethod
    def from_dict(cls, payload: dict[str, Any]):
        kind = payload.get("kind")
        if kind == cls.NodeInlineCode:
            inline_code = WorkflowNodeInlineCode.from_dict(payload.get("inline_code", {}))
            return WorkflowNode(kind=cls.NodeInlineCode, inline_code=inline_code)
        elif kind == cls.NodeLLMQuery:
            llm_query = WorkflowNodeLLMQuery.from_dict(payload.get("llm_query", {}))
            return WorkflowNode(kind=cls.NodeLLMQuery, llm_query=llm_query)
        elif kind == cls.NodeVectorSearch:
            vector_search = WorkflowNodeVectorSearch.from_dict(payload.get("vector_search", {}))
            return WorkflowNode(kind=cls.NodeVectorSearch, vector_search=vector_search)

    def to_v1_workflow_node_input(self) -> V1WorkflowNodeInput:
        return V1WorkflowNodeInput(
            kind=self.kind,
            inline_code=self.inline_code.to_v1_workflow_node_inline_code() if self.inline_code else None,
            llm_query=self.llm_query.to_v1_workflow_node_llm_query() if self.llm_query else None,
            vector_search=self.vector_search.to_v1_workflow_node_vector_search() if self.vector_search else None
        )


class SingleWorkflowVariable(object):
    source: Literal["text", "secret"]
    text: Optional[str]
    secret: Optional[str]
    resolved: Optional[str]

    def __init__(self, source: Literal["text", "secret"], text: Optional[str], secret: Optional[str],
                 resolved: Optional[str] = None):
        self.source = source
        self.text = text
        self.secret = secret
        self.resolved = resolved

    def to_v1_variable_value_input(self):
        return V1VariableValueInput(
            source=self.source,
            text=self.text,
            secret=self.secret,
        )


class Workflow(object):
    variables: dict[str, SingleWorkflowVariable]
    nodes: dict[str, WorkflowNode]
    edges: dict[str, list[WorkflowEdge]]
    permission_config: connection.PermissionConfig

    def __init__(self, nodes: dict[str, WorkflowNode], edges: dict[str, list[WorkflowEdge]],
                 variables: dict[str, SingleWorkflowVariable], permission_config: connection.PermissionConfig):
        self.nodes = nodes
        self.edges = edges
        self.variables = variables
        self.permission_config = permission_config


class WorkflowSpecInput(object):
    kind: Literal["workflowv1/Workflow"]
    variables: dict[str, SingleWorkflowVariable]
    nodes: dict[str, WorkflowNode]
    edges: dict[str, list[WorkflowEdge]]

    def __init__(self, kind: Literal["workflowv1/Workflow"], variables: dict[str, SingleWorkflowVariable],
                 nodes: dict[str, WorkflowNode], edges: dict[str, list[WorkflowEdge]]):
        self.kind = kind
        self.variables = variables
        self.nodes = nodes
        self.edges = edges

    @classmethod
    def from_dict(cls, spec_input: dict[str, Any]):
        raw_variables = spec_input.get("variables", {})
        variables = dict()
        for k, v in raw_variables.items():
            variables[k] = SingleWorkflowVariable(
                v["source"], v.get("text"), v.get("secret"), v.get("resolved"))
        raw_nodes = spec_input.get("nodes", {})
        nodes = dict()
        for k, v in raw_nodes.items():
            nodes[k] = WorkflowNode.from_dict(v)
        raw_edges = spec_input.get("edges", {})
        edges = dict()
        for k, v in raw_edges.items():
            edges[k] = [WorkflowEdge.from_dict(e) for e in v]
        return cls(kind="workflowv1/Workflow", variables=variables, nodes=nodes, edges=edges)

    def to_v1_workflow_revision_input(self):
        return V1WorkflowRevisionInput(
            kind=self.kind,
            variables={k: v.to_v1_variable_value_input() for k, v in self.variables.items()},
            nodes={k: v.to_v1_workflow_node_input() for k, v in self.nodes.items()},
            edges={k: [e.to_v1_single_workflow_edge_input() for e in edges] for k, edges in self.edges.items()},
        )
