import logging
from enum import Enum
from typing_extensions import Literal

from scale_gp._utils import is_dict
from scale_gp.types.application_edge_param import ApplicationEdgeParam
from scale_gp.types.application_node_param import ApplicationNodeParam
from scale_gp.types.application_configuration_param import ApplicationConfigurationParam

from .._client import SGPClient
from .._models import BaseModel

log: logging.Logger = logging.getLogger("scale_gp")


class ApplicationTemplate(BaseModel):
    """
    ### Description
    ApplicationTemplate describes the pre-defined available application templates that can be created by the ApplicationBuilder
    ### Parameters
    - application_type: The type of the predefined application template, currently supports "COMPLETION" and "RAG"
    - variant_id: The id of the application variant created by the ApplicationBuilder
    """

    application_type: Literal["COMPLETION", "RAG"]
    variant_id: str


class ApplicationBuilderNodeIDs(Enum):
    input_node_id = "input_node"
    completion_node_id = "completion_node"
    output_node_id = "output_node"
    prompt_engineering_node_id = "prompt_engineering_node"
    reranker_node_id = "reranker_node"
    knowledge_base_node_id = "knowledge_base_node"


class ApplicationBuilder:
    """
    ### Description
    ApplicationBuilder helps users quickly create predefined applications based on templates
    From the template, users can also easily call the process function without having to know what input fields are required
    """

    def __init__(self, client: SGPClient):
        self.client = client
        self.application = None

    def create_completion_application(
        self, *, account_id: str, application_name: str, completion_model_id: str
    ) -> ApplicationTemplate:
        """
        ### Description
        Creates a simple completion or chat completion application, the equivalent of Input -> Completion Model -> Output

        ### Parameters
        - account_id: The account id of the user
        - application_name: The name of the application
        - completion_model_id: The model deployment id of the completion model to use
        """

        # create application spec, this is the base for the application variant
        application_spec_id = self._create_app_spec(account_id=account_id, application_name=application_name)

        # create application variant config for a simple completion app
        edges = [
            ApplicationEdgeParam(
                from_node=ApplicationBuilderNodeIDs.input_node_id.value,
                to_node=ApplicationBuilderNodeIDs.completion_node_id.value,
                from_field="input-text",
                to_field="prompt",
            ),
            ApplicationEdgeParam(
                from_node=ApplicationBuilderNodeIDs.completion_node_id.value,
                to_node=ApplicationBuilderNodeIDs.output_node_id.value,
                from_field="completion",
                to_field="output-text",
            ),
        ]

        nodes = [
            ApplicationNodeParam(
                id=ApplicationBuilderNodeIDs.input_node_id.value,
                application_node_schema_id="text_input_schema",
                configuration={"input-text": {"value": "Completion prompt"}},
            ),
            ApplicationNodeParam(
                id=ApplicationBuilderNodeIDs.completion_node_id.value,
                application_node_schema_id="completion_model_schema",
                configuration={
                    "completion_model_id": {
                        "value": completion_model_id,
                    }
                },
            ),
            ApplicationNodeParam(
                id=ApplicationBuilderNodeIDs.output_node_id.value,
                application_node_schema_id="text_output_schema",
                configuration={"completion": {"value": "completion result"}},
            ),
        ]
        configuration = ApplicationConfigurationParam(edges=edges, nodes=nodes)

        application_variant = self.client.application_variants.create(
            account_id=account_id,
            application_spec_id=application_spec_id,
            name=application_name,
            version="V0",
            description="Automatically created completion application variant for " + application_name,
            configuration=configuration,
        )
        self.application = ApplicationTemplate(application_type="COMPLETION", variant_id=application_variant.id)
        log.info(f"\nCreated completion application for account {account_id}\nApp Variant ID: {application_variant.id}")
        return self.application

    def create_rag_application(
        self,
        *,
        account_id: str,
        application_name: str,
        knowledge_base_id: str,
        knowledge_base_top_k: int,
        reranker_model_id: str,
        reranker_top_k: int,
        prompt_engineering_template: str,
        completion_model_id: str,
    ) -> ApplicationTemplate:
        """
        ### Description
        Creates a simple RAG application, the equivalent of Input -> Knowledge Base -> Reranker -> Prompt Engineering -> Completion Model -> Output

        ### Parameters
        - account_id: The account id of the user
        - application_name: The name of the application
        - knowledge_base_id: The knowledge base id to use
        - knowledge_base_top_k: The top k parameter to use when querying the knowledge base
        - reranker_model_id: The model deployment id of the reranker model to use
        - reranker_top_k: The top k parameter to use with the reranker model
        - prompt_engineering_template: The prompt engineering template to use. Refer to https://mustache.github.io/mustache.5.html for more details
        - completion_model_id: The model deployment id of the completion model to use
        """

        # create application spec which is the base for the application variant
        application_spec_id = self._create_app_spec(account_id=account_id, application_name=application_name)

        edges = [
            ApplicationEdgeParam(
                from_node=ApplicationBuilderNodeIDs.input_node_id.value,
                to_node=ApplicationBuilderNodeIDs.knowledge_base_node_id.value,
                from_field="input-text",
                to_field="query",
            ),
            ApplicationEdgeParam(
                from_node=ApplicationBuilderNodeIDs.input_node_id.value,
                to_node=ApplicationBuilderNodeIDs.prompt_engineering_node_id.value,
                from_field="input-text",
                to_field="query",
            ),
            ApplicationEdgeParam(
                from_node=ApplicationBuilderNodeIDs.knowledge_base_node_id.value,
                to_node=ApplicationBuilderNodeIDs.reranker_node_id.value,
                from_field="chunks",
                to_field="chunks",
            ),
            ApplicationEdgeParam(
                from_node=ApplicationBuilderNodeIDs.input_node_id.value,
                to_node=ApplicationBuilderNodeIDs.reranker_node_id.value,
                from_field="input-text",
                to_field="prompt",
            ),
            ApplicationEdgeParam(
                from_node=ApplicationBuilderNodeIDs.reranker_node_id.value,
                to_node=ApplicationBuilderNodeIDs.prompt_engineering_node_id.value,
                from_field="chunks",
                to_field="chunks",
            ),
            ApplicationEdgeParam(
                from_node=ApplicationBuilderNodeIDs.prompt_engineering_node_id.value,
                to_node=ApplicationBuilderNodeIDs.completion_node_id.value,
                from_field="prompt",
                to_field="prompt",
            ),
            ApplicationEdgeParam(
                from_node=ApplicationBuilderNodeIDs.completion_node_id.value,
                to_node=ApplicationBuilderNodeIDs.output_node_id.value,
                from_field="completion",
                to_field="output-text",
            ),
            ApplicationEdgeParam(
                from_node=ApplicationBuilderNodeIDs.reranker_node_id.value,
                to_node=ApplicationBuilderNodeIDs.output_node_id.value,
                from_field="chunks",
                to_field="metadata",
            ),
        ]

        nodes = [
            ApplicationNodeParam(
                id=ApplicationBuilderNodeIDs.prompt_engineering_node_id.value,
                application_node_schema_id="prompt_engineering_schema",
                configuration={"prompt_template": {"value": "TEXT", "value": prompt_engineering_template}},
            ),
            ApplicationNodeParam(
                id=ApplicationBuilderNodeIDs.input_node_id.value,
                application_node_schema_id="text_input_schema",
                configuration={"input-text": {"value": "input-text"}},
            ),
            ApplicationNodeParam(
                id=ApplicationBuilderNodeIDs.completion_node_id.value,
                application_node_schema_id="completion_model_schema",
                configuration={
                    "completion_model_id": {
                        "value": completion_model_id,
                    }
                },
            ),
            ApplicationNodeParam(
                id=ApplicationBuilderNodeIDs.knowledge_base_node_id.value,
                application_node_schema_id="knowledge_base_schema",
                configuration={
                    "kb_id": {
                        "value": knowledge_base_id,
                    },
                    "top_k": {
                        "value": knowledge_base_top_k,
                    },
                },
            ),
            ApplicationNodeParam(
                id=ApplicationBuilderNodeIDs.reranker_node_id.value,
                application_node_schema_id="reranker_schema",
                configuration={
                    "reranking_model_id": {
                        "value": reranker_model_id,
                    },
                    "top_k": {
                        "value": reranker_top_k,
                    },
                },
            ),
            ApplicationNodeParam(
                id=ApplicationBuilderNodeIDs.output_node_id.value,
                application_node_schema_id="text_output_schema",
                configuration={"completion": {"value": "completion result"}},
            ),
        ]
        configuration = ApplicationConfigurationParam(edges=edges, nodes=nodes)

        application_variant = self.client.application_variants.create(
            account_id=account_id,
            application_spec_id=application_spec_id,
            name=application_name,
            version="V0",
            description="Automatically created rag application variant for " + application_name,
            configuration=configuration,
        )
        self.application = ApplicationTemplate(application_type="RAG", variant_id=application_variant.id)
        log.info(f"\nCreated RAG application for account {account_id}\nApp Variant ID: {application_variant.id}")
        return self.application

    def process(self, *, query: str) -> str:
        if not self.application:
            raise ValueError(
                "Application not created - you need to create the app with one of the create_ methods on this class before processing."
            )

        # call the application based on the application type
        if self.application.application_type == "COMPLETION":
            variant_response = self.client.application_variants.process(
                application_variant_id=self.application.variant_id,
                inputs={ApplicationBuilderNodeIDs.input_node_id.value: {"input-text": query}},
            )
            if not is_dict(variant_response):
                raise TypeError(f"Expected completion response to be a dictionary but got {variant_response!r}")

            completion_response = str(variant_response["output-text"])
            log.info(f"\nProcessed completion application\nApp Variant ID: {self.application.variant_id}")
            return completion_response
        elif self.application.application_type == "RAG":
            variant_response = self.client.application_variants.process(
                application_variant_id=self.application.variant_id,
                inputs={ApplicationBuilderNodeIDs.input_node_id.value: {"input-text": query}},
            )
            if not is_dict(variant_response):
                raise TypeError(f"Expected RAG response to be a dictionary but got {variant_response!r}")

            rag_response = str(variant_response["output-text"])
            log.info(f"\nProcessed RAG application\nApp Variant ID: {self.application.variant_id}")
            return rag_response
        else:
            raise ValueError("Unsupported application type")

    def _create_app_spec(self, *, account_id: str, application_name: str) -> str:
        application_spec = self.client.application_specs.create(
            account_id=account_id,
            description="Automatically created applicaton spec for " + application_name,
            name=application_name,
        )
        return application_spec.id
