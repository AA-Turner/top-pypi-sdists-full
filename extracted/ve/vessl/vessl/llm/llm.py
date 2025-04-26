from typing import Any

import vessl.llm.connection as connection
import vessl.llm.document as document
import vessl.llm.workflow as workflow

from openapi_client import LlmLLMWorkflowWorkloadReadConfigurationResponse, ProtoLLMWorkflowRevision, \
    V1WorkflowRevisionSpec, V1WorkflowNodeStruct, \
    ProtoLLMModelConnection, ProtoLLMVectorDBConnConfig, \
    ProtoLLMWorkloadConnectionConfiguration, V1VariableValue, LlmLLMKnowledgeIngestionConfigReadResponse, \
    LlmLLMKnowledgeRetrieverConfigReadResponse, LLMAPIKeyVerifyAPIInput, LlmLLMAPIKeyVerifyResponse, \
    LlmLLMWorkflowWorkloadReadTestConfigurationResponse, LLMWorkflowWorkloadReadTestConfigurationAPIInput, \
    ProtoRevealedSecret
from vessl.llm.knowledge import Knowledge
from vessl.llm.ingestion import IngestionConfig
from vessl.llm.retriever import RetrieverConfig
from vessl.util.exception import InvalidParamsError

from vessl.util.exception import InvalidOrganizationError
from vessl import vessl_api


def _build_workflow_from_configuration(revision_spec: V1WorkflowRevisionSpec,
                                       config: ProtoLLMWorkloadConnectionConfiguration,
                                       resolved_variables: dict[str, str]) -> workflow.Workflow:
    workflow_nodes: dict[str, workflow.WorkflowNode] = dict()
    for node_name, n in revision_spec.nodes.items():
        node: V1WorkflowNodeStruct = n
        model_connection_config: ProtoLLMModelConnection = config.model_connection_configs.get(node_name, None)
        model_connection = None
        if model_connection_config:
            model_connection = connection.ModelConnection(model_connection=model_connection_config)
        vector_db_connection: ProtoLLMVectorDBConnConfig = config.vector_db_connection_configs.get(node_name, None)
        vector_db = None
        permission = None
        if vector_db_connection:
            collection_name = config.vector_db_collections[node_name]
            vector_db = connection.VectorDBConnection(vector_db=vector_db_connection, collection_name=collection_name)
            permission = connection.PermissionConfig(config.knowledge_permission_configs[node_name])
        workflow_nodes[node_name] = workflow.WorkflowNode.from_config(node=node, model_connection=model_connection,
                                                                      vector_db=vector_db,
                                                                      permission=permission)

    workflow_edges: dict[str, list[workflow.WorkflowEdge]] = dict()
    for node_name, edges in revision_spec.edges.items():
        workflow_edges[node_name] = [workflow.WorkflowEdge.from_config(e) for e in edges]

    variables: dict[str, workflow.SingleWorkflowVariable] = dict()
    variable_specs: dict[str, V1VariableValue] = revision_spec.variables
    for variable_name, var in variable_specs.items():
        if var.source == "text":
            variables[variable_name] = workflow.SingleWorkflowVariable(
                'text', var.text, var.secret, resolved_variables.get(variable_name))

    return workflow.Workflow(nodes=workflow_nodes, edges=workflow_edges, variables=variables,
                             permission_config=config.workflow_permission_config)


def read_test_workflow_configuration(raw_spec_input: dict[str, Any]) -> workflow.Workflow:
    """
    Read the workflow configuration from api server.
    Args:
        raw_spec_input(dict): Raw spec input.
    Example:
        ```python
        vessl.read_test_workflow_configuration()
        ```
    """
    spec_input = workflow.WorkflowSpecInput.from_dict(raw_spec_input).to_v1_workflow_revision_input()
    req = LLMWorkflowWorkloadReadTestConfigurationAPIInput(spec_input=spec_input)
    workflow_test_config: LlmLLMWorkflowWorkloadReadTestConfigurationResponse = \
        vessl_api.l_lm_workflow_workload_read_test_configuration_api(
            llm_workflow_workload_read_test_configuration_api_input=req,
        )
    revision_spec: V1WorkflowRevisionSpec = workflow_test_config.workflow_spec
    connection_config: ProtoLLMWorkloadConnectionConfiguration = workflow_test_config.config
    resolved_variables: dict[str, str] = workflow_test_config.variables
    return _build_workflow_from_configuration(revision_spec, connection_config, resolved_variables)


def read_workflow_configuration() -> workflow.Workflow:
    """
    Read the workflow configuration from api server.
    Args:
        None
    Example:
        ```python
        vessl.read_workflow_configuration()
        ```
    """
    workflow_config: LlmLLMWorkflowWorkloadReadConfigurationResponse = \
        vessl_api.l_lm_workflow_workload_read_configuration_api()
    revision: ProtoLLMWorkflowRevision = workflow_config.workflow_revision
    revision_spec: V1WorkflowRevisionSpec = revision.spec
    config: ProtoLLMWorkloadConnectionConfiguration = workflow_config.config
    variables: dict[str, str] = workflow_config.variables
    return _build_workflow_from_configuration(revision_spec, config, variables)


def read_ingestion_job_configuration() -> IngestionConfig:
    config: LlmLLMKnowledgeIngestionConfigReadResponse = vessl_api.l_lm_knowledge_ingestion_config_read_api()

    knowledge = None
    if config.knowledge is not None:
        knowledge_config = config.knowledge
        knowledge = Knowledge(knowledge=knowledge_config)

    vector_db = None
    if config.vector_db_connection is not None and config.knowledge is not None:
        vector_db_config = config.vector_db_connection
        vector_db = connection.VectorDBConnection(vector_db=vector_db_config,
                                                  collection_name=config.knowledge.vectordb_collection_name)

    model_connection = None
    if config.model_connection is not None:
        model_connection_config: ProtoLLMModelConnection = config.model_connection
        model_connection = connection.ModelConnection(model_connection=model_connection_config)

    documents = []
    if config.documents is not None:
        documents = [document.Document(doc) for doc in config.documents]

    return IngestionConfig(llm_knowledge=knowledge, llm_model=model_connection, vector_db=vector_db,
                           documents=documents)


def read_retriever_configuration() -> RetrieverConfig:
    config: LlmLLMKnowledgeRetrieverConfigReadResponse = vessl_api.l_lm_knowledge_retriever_config_read_api()

    knowledge = None
    if config.knowledge is not None:
        knowledge_config = config.knowledge
        knowledge = Knowledge(knowledge=knowledge_config)

    vector_db = None
    if config.vector_db_connection is not None and config.knowledge is not None:
        vector_db_config = config.vector_db_connection
        vector_db = connection.VectorDBConnection(vector_db=vector_db_config,
                                                  collection_name=config.knowledge.vectordb_collection_name)

    model_connection = None
    if config.model_connection is not None:
        model_connection_config: ProtoLLMModelConnection = config.model_connection
        model_connection = connection.ModelConnection(model_connection=model_connection_config)

    return RetrieverConfig(llm_knowledge=knowledge, llm_model=model_connection, vector_db=vector_db)


def update_job_status(job_number: int, message: str, status: str, **kwargs):
    """
    Update the job status.
    Args:
        job_number(int): Job number.
        message(str): Message.
        status(str): Status.

    Example:
        ```python
        vessl.update_job_status(
            job_number=1,
            message="job completed",
            status="completed",
            organization_name="foo",
            knowledge_name="bar",
        )
        ```
    """
    return vessl_api.l_lm_knowledge_ingestion_job_status_update_api(
        knowledge_name=kwargs.get("knowledge_name"),
        organization_name=_get_organization_name(**kwargs),
        job_number=job_number,
        llm_knowledge_ingestion_job_status_update_api_input={
            "status": status,
            "message": message,
        }
    )


def verify_llm_api_key(api_key: str) -> connection.UserGroup:
    """
    Verify the api key.
    Args:
        api_key(str): Decrypted API key.

    Example:
        ```python
        vessl.verify_llm__api_key(api_key="foo")
        ```
    """

    resp: LlmLLMAPIKeyVerifyResponse = vessl_api.l_lmapi_key_verify_api(
        llmapi_key_verify_api_input=LLMAPIKeyVerifyAPIInput(api_key=api_key))

    if not resp.is_verified:
        raise InvalidParamsError("API key verification failed.")

    return connection.UserGroup(resp.user_group)


def _get_organization_name(**kwargs) -> str:
    organization_name = kwargs.get("organization_name")
    if organization_name is not None:
        return organization_name
    if vessl_api.organization is not None:
        return vessl_api.organization.name
    if vessl_api.run_execution_default_organization is not None:
        return vessl_api.run_execution_default_organization
    raise InvalidOrganizationError("No organization selected.")
