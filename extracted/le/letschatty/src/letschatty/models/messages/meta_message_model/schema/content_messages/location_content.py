from pydantic import BaseModel

class MetaLocationContent(BaseModel):
    latitude: float
    longitude: float

    address: str = None
    url: str = None
    name: str = None

    def is_location_fixed(self) -> bool:
        return bool(self.address and self.url and self.name)
    
    def is_location_shared(self) -> bool:
        return bool(not self.address and not self.url and not self.name)
    