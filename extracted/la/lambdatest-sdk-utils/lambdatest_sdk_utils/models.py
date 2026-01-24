from typing import Optional
from dataclasses import dataclass


@dataclass
class BuildData:
    """Build data from SmartUI API response."""
    build_id: Optional[str] = None
    build_url: Optional[str] = None
    baseline: Optional[bool] = None
    name: Optional[str] = None
    project_token: Optional[str] = None

    def to_dict(self):
        return {
            "buildId": self.build_id,
            "buildURL": self.build_url,
            "baseline": self.baseline,
            "buildName": self.name
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            build_id=data.get("buildId"),
            build_url=data.get("buildURL"),
            baseline=data.get("baseline"),
            name=data.get("buildName"),
            project_token=data.get("projectToken")
        )


@dataclass
class BuildResponse:
    """Response from build creation API."""
    data: Optional[BuildData] = None

    @classmethod
    def from_dict(cls, data: dict):
        build_data = None
        if "data" in data:
            build_data = BuildData.from_dict(data["data"])
        return cls(data=build_data)


@dataclass
class UploadSnapshotRequest:
    """Request object for uploading screenshots."""
    browser_name: Optional[str] = None
    os: Optional[str] = None
    viewport: Optional[str] = None
    project_token: Optional[str] = None
    build_id: Optional[str] = None
    build_name: Optional[str] = None
    screenshot_name: Optional[str] = None
    screenshot_hash: Optional[str] = None
    device_name: Optional[str] = None
    full_page: Optional[str] = None
    is_last_chunk: Optional[str] = None
    chunk_count: Optional[int] = None
    upload_chunk: Optional[str] = None
    navigation_bar_height: Optional[str] = None
    status_bar_height: Optional[str] = None
    crop_footer: Optional[str] = "false"
    crop_status_bar: Optional[str] = "false"
    project_type: Optional[str] = None

    def to_dict(self):
        """Convert to dictionary for multipart form data."""
        data = {}
        if self.browser_name:
            data["browser"] = self.browser_name
        if self.os:
            data["os"] = self.os
        if self.viewport:
            data["viewport"] = self.viewport
        if self.build_id:
            data["buildId"] = self.build_id
        if self.build_name:
            data["buildName"] = self.build_name
        if self.screenshot_name:
            data["screenshotName"] = self.screenshot_name
        if self.screenshot_hash:
            data["screenshotHash"] = self.screenshot_hash
        if self.device_name:
            data["deviceName"] = self.device_name
        if self.full_page:
            data["fullPage"] = self.full_page
        if self.is_last_chunk:
            data["isLastChunk"] = self.is_last_chunk
        if self.chunk_count is not None:
            data["chunkCount"] = str(self.chunk_count)
        if self.upload_chunk:
            data["uploadChunk"] = self.upload_chunk
        if self.navigation_bar_height:
            data["navigationBarHeight"] = self.navigation_bar_height
        if self.status_bar_height:
            data["statusBarHeight"] = self.status_bar_height
        if self.crop_footer:
            data["cropFooter"] = self.crop_footer
        if self.crop_status_bar:
            data["cropStatusBar"] = self.crop_status_bar
        if self.project_type:
            data["projectType"] = self.project_type
        
        return data

