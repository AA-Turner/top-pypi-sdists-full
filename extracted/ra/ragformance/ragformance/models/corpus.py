from typing import Dict, Optional
from pydantic import BaseModel, Field


class DocModel(BaseModel):
    id: str = Field(alias="_id")
    title: str
    text: str
    metadata: Optional[Dict] = None

    def to_dict(self):
        return {
            "_id": self.id,
            "title": self.title,
            "text": self.text,
            "metadata": self.metadata,
        }
