import json
from typing import Any, List, Optional, Tuple, Union, overload

import pydantic
from gable.api.client import GableAPIClient
from gable.openapi import (
    ContractOutput,
    GableSchemaContractField,
    PostContractRequest,
    PostContractResponse,
)
from gable.sdk.converters.trino import (
    convert_trino_timestamp_to_spark_timestamp,
    trino_to_gable_type,
)

from .helpers import external_to_internal_contract_input
from .models import ContractPublishResponse, ExternalContractInput, TrinoDataType


class GableContract:
    def __init__(self, api_endpoint, api_key) -> None:
        self.api_client = GableAPIClient(api_endpoint, api_key)

    def publish(
        self,
        contracts: list[ExternalContractInput],
    ) -> ContractPublishResponse:
        api_response, success, _status_code = self.api_client.post_contract(
            PostContractRequest(
                __root__=[
                    external_to_internal_contract_input(contract)
                    for contract in contracts
                ],
            )
        )

        # Currently, the behavior is either all contracts are published or none are (if there is one invalid contract)
        # Ideally, we can refactor this code and the API to allow for partial success in the future

        if not success or not isinstance(api_response, PostContractResponse):
            failure_message = (
                api_response.message
                if isinstance(api_response, PostContractResponse)
                else "Unknown error"
            )
            return ContractPublishResponse(
                success=False, updatedContractIds=[], message=failure_message
            )
        else:
            updated_contract_ids = api_response.contractIds
            return ContractPublishResponse(
                success=True,
                updatedContractIds=updated_contract_ids,
                message=api_response.message,
            )

    @overload
    # The "*," argument forces the caller to use keyword arguments
    def get_contract(self, *, contract_id: str) -> Optional[ContractOutput]: ...

    @overload
    # The "*," argument forces the caller to use keyword arguments
    def get_contract(
        self, *, domain: str, contract_name: str, status: Optional[str] = None
    ) -> Optional[ContractOutput]: ...

    def get_contract(self, **kwargs) -> Optional[ContractOutput]:
        """
        Get a contract by ID or by domain and name.
        
        Args:
            **kwargs: Either contract_id or (domain + contract_name) must be provided.
                     Optionally, status can be provided to filter contracts by status
                     when searching by domain and name.
        
        Examples:
            # Get by contract ID
            contract = client.contracts.get_contract(contract_id="123")
            
            # Get by domain and name
            contract = client.contracts.get_contract(domain="my_domain", contract_name="my_contract")
            
            # Get by domain and name with specific status filter
            contract = client.contracts.get_contract(
                domain="my_domain", 
                contract_name="my_contract", 
                status="ACTIVE,DRAFT"
            )
        """
        if "contract_id" in kwargs:
            return self.api_client.get_contract(kwargs["contract_id"])
        elif "domain" in kwargs and "contract_name" in kwargs:
            # TODO: This is not efficient, we should add a filter in the API
            status = kwargs.get("status")
            source_type_contracts = self.api_client.get_contracts(status=status)
            for contract in source_type_contracts:
                if (
                    contract.contractSpec.namespace == kwargs["domain"]
                    and contract.contractSpec.name == kwargs["contract_name"]
                ):
                    return contract
            return None
        raise ValueError("Either contract_id or (domain + contract_name) must be set")

    def get_contracts(
        self,
        search: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None,
        order_dir: Optional[str] = None,
        status: Optional[str] = None,
    ) -> List[ContractOutput]:
        return self.api_client.get_contracts(
            search=search,
            limit=limit,
            offset=offset,
            order_by=order_by,
            order_dir=order_dir,
            status=status,
        )

    @staticmethod
    def trino_to_gable_schema(
        dict_schema: dict[
            str, Union[str, Union[TrinoDataType, Tuple[TrinoDataType, Tuple[Any, ...]]]]
        ],
        convert_to_spark_types: bool = False,
    ) -> List[GableSchemaContractField]:
        results = [
            trino_to_gable_type(key, value) for key, value in dict_schema.items()
        ]
        if convert_to_spark_types:
            results = [
                convert_trino_timestamp_to_spark_timestamp(result) for result in results
            ]
        return results

    @staticmethod
    def json_schema_to_gable_schema(
        schema: Union[str, dict[str, Any]],
    ) -> List[GableSchemaContractField]:
        import recap
        import recap.types
        from recap.converters.json_schema import JSONSchemaConverter

        # JSONSchemaConverter expects a string, so serialize if it's a dict
        if isinstance(schema, dict):
            schema = json.dumps(schema)
        converter = JSONSchemaConverter()

        return [
            pydantic.parse_obj_as(GableSchemaContractField, recap.types.to_dict(o))
            for o in converter.to_recap(schema).fields
        ]
