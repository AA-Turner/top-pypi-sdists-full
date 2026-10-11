"""
Merge API operations for DealCloud.

The Merge API enables combining duplicate entries:
- Merge multiple entries into one "winner"
- Transfer relationships to winner
- Optionally delete "loser" entries

Only merge_entries (POST merge/{entryTypeId}) is supported by the API.
See: https://api.docs.dealcloud.com/docs - Data/Merge API
"""

from typing import List, Optional, Union

from ..relationshipintelligence.dealcloud_ri import DealCloudRelationshipIntelligence


class DealCloudMerge(DealCloudRelationshipIntelligence):
    """
    One link in the linear inheritance chain; parent order is for composition
    (single DealCloud client gets all features), not dependency. Avoids mixins.
    Merge API operations.
    
    Provides duplicate entry merging functionality.
    """
    
    @property
    def merge_url(self) -> str:
        """
        Get the Merge API base URL.
        
        Use this for custom merge API calls. Only POST to merge/{entryTypeId} is supported.
        
        Returns:
            str: Merge API URL (e.g., "https://site.dealcloud.com/api/rest/v4/data/merge")
        """
        return self._merge_url
    
    # =========================================================================
    # Merge Operations
    # =========================================================================
    
    def merge_entries(
        self,
        object_id: Union[int, str],
        winner_entry_id: int,
        loser_entry_ids: List[int],
        field_overrides: Optional[dict] = None,
        delete_losers: bool = True,
        transfer_relationships: bool = True,
        overwrite_empty_values: Optional[bool] = None,
    ) -> dict:
        """
        Merge duplicate entries into a winner record.

        API: POST .../data/merge/{entryTypeId}. Body is an array of MergeEntriesRequestVm:
        [{ "entryId": winnerId, "mergeEntries": [loserId, ...] }]. Query: overwriteEmptyValues.
        The API always merges losers into the winner; delete_losers and transfer_relationships
        are accepted for compatibility but not sent (API behavior is fixed).

        Args:
            object_id: Object type (ID or API name)
            winner_entry_id: Entry ID to keep and merge into
            loser_entry_ids: Entry IDs to merge from (merged into winner; API limit 10 per item)
            field_overrides: Ignored (not in swagger); reserved for future use
            delete_losers: Ignored (API always merges/deletes losers); kept for signature compat
            transfer_relationships: Ignored (API transfers refs to winner); kept for signature compat
            overwrite_empty_values: If True, migrate values from losers to fill blank winner fields (query param; only when merging exactly 2 entries per docs)

        Returns:
            Response from POST (200 on success)
        """
        url = f"{self._merge_url}/{object_id}"
        # Swagger: body is array of { entryId, mergeEntries }; max 10 in mergeEntries per item
        item = {
            "entryId": winner_entry_id,
            "mergeEntries": loser_entry_ids[:10],
        }
        if field_overrides is not None:
            item["fieldOverrides"] = field_overrides
        item["deleteLoserEntries"] = delete_losers
        item["transferRelationships"] = transfer_relationships
        payload = [item]
        params = None
        if overwrite_empty_values is not None:
            params = {"overwriteEmptyValues": overwrite_empty_values}
        return self._client.post(url, json=payload, params=params)

