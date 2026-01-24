import os
import requests
from typing import Optional, Dict
from lambdatest_sdk_utils.logger import get_logger
from lambdatest_sdk_utils.models import BuildResponse, BuildData, UploadSnapshotRequest
from lambdatest_sdk_utils.git_utils import GitInfo

logger = get_logger('lambdatest_sdk_utils')

# API URLs
SMARTUI_CLIENT_API_URL = os.getenv("SMARTUI_CLIENT_API_URL", "https://api.lambdatest.com/visualui/1.0")
SMARTUI_UPLOAD_URL = os.getenv("SMARTUI_UPLOAD_URL", "https://api.lambdatest.com/")
TEST_TYPE = "lambdatest-java-app-sdk"

# Routes
SMARTUI_AUTH_ROUTE = "/token/verify"
SMARTUI_CREATE_BUILD = "/build"
SMARTUI_UPLOAD_SCREENSHOT_ROUTE = "/screenshot"
SMARTUI_FINALISE_BUILD_ROUTE = "/build"


def get_host_url() -> str:
    """Get host URL from environment or use default."""
    return os.getenv("SMARTUI_CLIENT_API_URL", SMARTUI_CLIENT_API_URL)


def get_upload_host_url() -> str:
    """Get upload host URL from environment or use default."""
    return os.getenv("SMARTUI_UPLOAD_URL", SMARTUI_UPLOAD_URL)


def is_user_authenticated(project_token: str) -> bool:
    """
    Verify if the project token is valid.
    
    Args:
        project_token: LambdaTest project token
        
    Returns:
        True if authenticated, False otherwise
    """
    try:
        url = get_host_url() + SMARTUI_AUTH_ROUTE
        headers = {"projectToken": project_token}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return True
    except Exception as e:
        logger.error(f"Authentication failed: {e}")
        return False


def create_build(git_info: Optional[GitInfo], project_token: str, 
                 options: Optional[Dict[str, str]] = None) -> BuildResponse:
    """
    Create a build in SmartUI.
    
    Args:
        git_info: Git information object
        project_token: LambdaTest project token
        options: Optional build options (e.g., buildName)
        
    Returns:
        BuildResponse object with build data
        
    Raises:
        Exception: If build creation fails
    """
    if options is None:
        options = {}
    
    # Verify authentication
    if not is_user_authenticated(project_token):
        raise Exception("User authentication failed")
    
    # Prepare build request
    build_name = options.get("buildName", "")
    if not build_name or not build_name.strip():
        import uuid
        build_name = f"smartui-{str(uuid.uuid4())[:10]}"
        logger.info(f"Build name set from system: {build_name}")
    else:
        logger.info(f"Build name set from options: {build_name}")
    
    build_request = {
        "buildName": build_name
    }
    
    if git_info:
        build_request["git"] = git_info.to_dict()
    
    # Make API call
    try:
        url = get_host_url() + SMARTUI_CREATE_BUILD
        headers = {"projectToken": project_token, "Content-Type": "application/json"}
        response = requests.post(url, json=build_request, headers=headers, timeout=30)
        response.raise_for_status()
        
        response_data = response.json()
        build_response = BuildResponse.from_dict(response_data)
        
        if build_response.data:
            logger.info(f"Build ID set: {build_response.data.build_id} for build name: {build_response.data.name}")
        else:
            raise Exception(f"Build not created for projectToken: {project_token}")
        
        return build_response
    except Exception as e:
        logger.error(f"Couldn't create smartui build: {e}")
        raise Exception(f"Couldn't create smartui build: {e}")


def upload_screenshot(screenshot_path: str, upload_request: UploadSnapshotRequest, 
                     build_data: BuildData) -> None:
    """
    Upload a screenshot to SmartUI.
    
    Args:
        screenshot_path: Path to screenshot file
        upload_request: Upload request object with metadata
        build_data: Build data object
        
    Raises:
        Exception: If upload fails
    """
    try:
        url = get_host_url() + SMARTUI_UPLOAD_SCREENSHOT_ROUTE
        
        # Prepare multipart form data
        with open(screenshot_path, 'rb') as f:
            files = {
                'screenshot': (upload_request.screenshot_name, f, 'image/png')
            }
            
            data = upload_request.to_dict()
            # Add build-specific fields
            data["buildId"] = build_data.build_id
            data["buildName"] = build_data.name
            data["baseline"] = str(build_data.baseline).lower() if build_data.baseline is not None else "false"
            data["projectType"] = TEST_TYPE
            
            headers = {
                "projectToken": upload_request.project_token
            }
            
            response = requests.post(url, files=files, data=data, headers=headers, timeout=60)
            response.raise_for_status()
        
        logger.info(f"Screenshot uploaded successfully: {upload_request.screenshot_name}")
    except Exception as e:
        logger.error(f"Couldn't upload image to SmartUI: {e}")
        raise Exception(f"Couldn't upload image to SmartUI: {e}")


def stop_build(build_id: str, project_token: str) -> None:
    """
    Stop/finalize a build in SmartUI.
    
    Args:
        build_id: Build ID to stop
        project_token: LambdaTest project token
        
    Raises:
        Exception: If stop fails
    """
    try:
        url = f"{get_host_url()}{SMARTUI_FINALISE_BUILD_ROUTE}?buildId={build_id}&testType={TEST_TYPE}"
        headers = {"projectToken": project_token}
        response = requests.delete(url, headers=headers, timeout=30)
        response.raise_for_status()
        logger.info(f"Build stopped successfully: {build_id}")
    except Exception as e:
        logger.error(f"Couldn't stop the build: {e}")
        raise Exception(f"Failed to stop build due to: {e}")

