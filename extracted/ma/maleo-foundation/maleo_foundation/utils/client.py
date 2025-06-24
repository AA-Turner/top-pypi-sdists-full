import asyncio
from functools import wraps
from pydantic import ValidationError
from typing import Optional, Type, Union
from maleo_foundation.types import BaseTypes
from maleo_foundation.models.transfers.results.client.service import \
    BaseClientServiceResultsTransfers

class BaseClientUtils:
    @staticmethod
    def result_processor(
        fail_class: Type[BaseClientServiceResultsTransfers.Fail],
        data_found_class: Union[
            Type[BaseClientServiceResultsTransfers.SingleData],
            Type[BaseClientServiceResultsTransfers.UnpaginatedMultipleData],
            Type[BaseClientServiceResultsTransfers.PaginatedMultipleData]
        ],
        no_data_class: Optional[Type[BaseClientServiceResultsTransfers.NoData]] = None,
    ):
        """Decorator to handle repository-related exceptions consistently."""
        def decorator(func):
            def _processor(result: BaseTypes.StringToAnyDict):
                if "success" not in result and "data" not in result:
                    raise ValueError("Result did not have both 'success' and 'data' field")
                success:bool = result.get("success")
                data:BaseTypes.StringToAnyDict = result.get("data")
                if not success:
                    validated_result = fail_class.model_validate(result)
                    return validated_result
                else:
                    if data is None:
                        if no_data_class is None:
                            raise ValueError("'no_data_class' must be given to validate No Data")
                        validated_result = no_data_class.model_validate(result)
                        return validated_result
                    else:
                        validated_result = data_found_class.model_validate(result)
                        return validated_result
            if asyncio.iscoroutinefunction(func):
                @wraps(func)
                async def async_wrapper(*args, **kwargs):
                    try:
                        result: BaseTypes.StringToAnyDict = await func(*args, **kwargs)
                        return _processor(result=result)
                    except ValidationError as e:
                        raise
                    except Exception as e:
                        raise
                return async_wrapper
            else:
                @wraps(func)
                def sync_wrapper(*args, **kwargs):
                    try:
                        result: BaseTypes.StringToAnyDict = func(*args, **kwargs)
                        return _processor(result=result)
                    except ValidationError as e:
                        raise
                    except Exception as e:
                        raise
                return sync_wrapper
        return decorator