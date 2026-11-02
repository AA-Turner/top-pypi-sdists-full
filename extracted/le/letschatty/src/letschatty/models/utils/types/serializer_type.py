from enum import StrEnum

class SerializerType(StrEnum):
    FRONTEND = "frontend"
    DATABASE = "database"
    FRONTEND_ASSET_PREVIEW = "frontend_asset_preview"
    API = "api"
