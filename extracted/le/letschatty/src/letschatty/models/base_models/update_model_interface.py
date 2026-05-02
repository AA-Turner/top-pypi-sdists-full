from datetime import datetime
from zoneinfo import ZoneInfo
from pydantic import BaseModel
from typing import TypeVar
from .helpers import _normalize_precision
T = TypeVar('T', bound='UpdateableMixin')

class UpdateableMixin(BaseModel):
    """Interface for models that can be updated, creating a new instance. It automatically handles the updated_at timestamp and mantains the frozen fields"""
    def update_from_dict(self: T, **kwargs) -> T:
        """
        Updates non-frozen fields of the model with new values.
        Automatically handles the updated_at timestamp.
        
        Args:
            **kwargs: Fields to update and their new values
            
        Returns:
            A new instance of the model with updated values
        """
        # Get current model data
        current_data = self.model_dump(by_alias=True)
        
        # Get frozen field names
        frozen_fields = {
            field.alias or field_name for field_name, field in self.model_fields.items()
            if field.frozen
        }
        
        # Remove any frozen fields from updates
        updates = {k: v for k, v in kwargs.items() if k not in frozen_fields}
        
        # Always update the updated_at timestamp if it exists in the model
        if 'updated_at' in self.model_fields:
            updates['updated_at'] = _normalize_precision(datetime.now(ZoneInfo("UTC")))
            
        # Merge current data with updates
        new_data = {**current_data, **updates}
        
        # Create new instance
        return self.__class__(**new_data)
    
    def update(self: T, other: T) -> T:
        """
        Updates the model with the values of another model.
        """
        return self.update_from_dict(**other.model_dump(by_alias=True))

