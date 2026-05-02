from ...base_models.chatty_asset_model import CompanyAssetModel
from ...utils.types.identifier import StrObjectId

class FriendlyCodeForSource(CompanyAssetModel):
    """Used to map a code to a source for friendly urls"""
    friendly_code: str
    source_id: StrObjectId