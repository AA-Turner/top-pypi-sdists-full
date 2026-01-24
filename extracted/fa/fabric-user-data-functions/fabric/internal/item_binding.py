import json
from typing import Any, Optional

# flake8: noqa: I900
import azure
from azure.functions.decorators.core import DataType, InputBinding

from fabric.functions.fabric_item import FabricItem
from fabric.internal.fabric_lakehouse_files_client import FabricLakehouseFilesClient
from fabric.functions.udf_exception import UserDataFunctionInternalError

from fabric.functions.fabric_class import (FabricSqlConnection, FabricLakehouseClient, FabricVariablesClient)

# The binding object that will be used by our input decorator below
class FabricItemInput(InputBinding):
    @staticmethod
    def get_binding_name() -> str:
        return 'FabricItem'
    
    def __init__(self,
                name: str,
                alias: Optional[str] = None,
                audienceType: Optional[str] = None,
                **kwargs):
        super().__init__(name, DataType.STRING)

# The input converter that automatically gets registered in the function app. 
class FabricItemConverter(azure.functions.meta.InConverter,
                              binding='FabricItem'):

    @classmethod
    def check_input_type_annotation(cls, pytype: type) -> bool:
        return True
    
    @classmethod
    def parseType(self, body: json):
        endpoints = body['Endpoints']
        endpoints = {k.lower(): v for k, v in endpoints.items()}  # we can know this doesn't have collisions 
        # because the host extension uses a case insensitive dictionary
        sqlEndpoint = "sqlendpoint"
        fileEndpoint = "fileendpoint"
        # endpoint keys are normalized to lowercase above, use lowercase key here
        vlEndpoint = "vlendpoint"
        

        if sqlEndpoint in endpoints and fileEndpoint in endpoints:
            return FabricLakehouseClient(
                alias_name=body['AliasName'],
                endpoints=endpoints,
            )
        elif sqlEndpoint in endpoints:
            return FabricSqlConnection(
                alias_name=body['AliasName'],
                endpoints=endpoints,
            )
        elif fileEndpoint in endpoints:
            return FabricLakehouseFilesClient(
                alias_name=body['AliasName'],
                endpoints=endpoints,
            )
        elif vlEndpoint in endpoints:
            # Validate expected keys to provide clearer errors during local testing
            vl_info = endpoints.get(vlEndpoint, {})
            if not isinstance(vl_info, dict) or 'ConnectionString' not in vl_info or 'AccessToken' not in vl_info:
                raise UserDataFunctionInternalError(f"Invalid vlendpoint payload for alias {body.get('AliasName')}")
            return FabricVariablesClient(
                alias_name=body['AliasName'],
                endpoints=endpoints,
            )

        # If not found above, return the default
        return FabricItem(
            alias_name=body['AliasName'],
            endpoints=endpoints)
    
    @classmethod
    def decode(cls, data, *,
               trigger_metadata) -> Any:
        if data is not None and data.type == 'string' and data.value is not None: 
            body = json.loads(data.value)
            error = body.get('ErrorMessage', None)
            if error:
                return UserDataFunctionInternalError(
                    f'Unable to load data successfully for fabric item', {'reason': error})
        else:
            return UserDataFunctionInternalError(
                f'Unable to load data successfully for fabric item')

        return cls.parseType(body)