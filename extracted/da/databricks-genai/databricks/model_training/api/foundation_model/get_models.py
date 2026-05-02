"""List multiple model training runs"""

from databricks.model_training.api.engine import get_return_response, run_singular_mapi_request
from databricks.model_training.types import TrainingConstants, TrainingModelConstants
from databricks.model_training.types.common import ObjectList, ObjectType

QUERY_FUNCTION = 'getFinetuneConstants'

QUERY = f"""
query Models {{
  {QUERY_FUNCTION} {{
    models {{
      name
      displayName
      maxContextLength
    }}
  }}
}}"""


def get_models() -> ObjectList[TrainingModelConstants]:
    """List available models (for the Foundation Model Training API) and their associated info

    Returns:
        ObjectList[ModelInfo]: A list of models and their associated info
    """
    response = run_singular_mapi_request(query=QUERY,
                                         query_function=QUERY_FUNCTION,
                                         return_model_type=TrainingConstants,
                                         variables={})

    return ObjectList(get_return_response(response).models, ObjectType.TRAINING_MODEL_CONSTANTS)
