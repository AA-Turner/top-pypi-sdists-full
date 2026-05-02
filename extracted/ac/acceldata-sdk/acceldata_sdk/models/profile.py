from enum import Enum
from typing import List, Optional, Dict, Any
from acceldata_sdk.models.common_types import ExecutionType, MarkerConfig

class Profile:

    def __init__(self, assetId, createdAt, id, jobId=None, profilingType=None, sparkClusterContext=None, status=None,
                 updatedAt=None, rows=None,
                 totalRows=None, jobType=None, autoProfileId=None, profileDataAvailable=None, marker=None,
                 profiledData=None, error=None, client=None, *args, **kwargs):
        self.client = client
        self.autoProfileId = autoProfileId
        self.profileDataAvailable = profileDataAvailable
        self.jobType = jobType
        self.updatedAt = updatedAt
        self.status = status
        self.sparkClusterContext = sparkClusterContext
        self.rows = rows
        self.profilingType = profilingType
        self.profiledData = profiledData
        self.marker = marker
        self.jobId = jobId
        self.id = id
        self.error = error
        self.createdAt = createdAt
        self.assetId = assetId
        self.totalRows = totalRows

    def __repr__(self):
        return f"Profile({self.__dict__})"

    def cancel(self):
        return self.client.cancel_profile(self.id)

    def get_status(self):
        return self.client.get_profile_request_details(asset_id=self.assetId, req_id=self.id)

class ProfilingType(Enum):
    SAMPLE = 'SELECTIVE'
    FULL = 'FULL'
    INCREMENTAL = 'INCREMENTAL'


class JobType(Enum):
    PROFILE = 'profile'
    MINI_PROFILE = 'mini-profile'
    # FULL = 'autotag'


class ProfileRequest:

    def __init__(self, id, status, createdAt=None, updatedAt=None, client=None, totalRows=None, isProfileAnomalous=None,
                 *args, **kwargs):
        self.client = client
        self.updatedAt = updatedAt
        self.createdAt = createdAt
        self.status = status
        self.id = id
        self.totalRows = totalRows
        self.isProfileAnomalous = isProfileAnomalous

    def __repr__(self):
        return f"ProfileRequest({self.__dict__})"

    def cancel(self):
        return self.client.cancel_profile(self.id)


class StartProfilingRequest:
    def __init__(self, profilingType: 'ExecutionType', markerConfig: 'MarkerConfig' = None, *args, **kwargs):
        """
        Initializes a StartProfilingRequest object.

        Args:
            profilingType (ExecutionType): The type of profiling to be executed.
            markerConfig (MarkerConfig, optional): The configuration for the markers. Defaults to None.
        """
        self.profilingType = profilingType
        self.markerConfig = markerConfig

    def to_dict(self) -> Dict[str, Any]:
        return {
            "data": {
                "profilingType": self.profilingType.to_dict(),
                "markerConfig": self.markerConfig.to_dict() if self.markerConfig else None
            }
        }
