from sage.utils import get_user_profile
from sage.utils.exceptions import ApiError

class ApiHandler:
    """
    Handles API interactions for the AI platform.
    """

    def __init__(self, api_key: str):
        """
        Initializes the API handler with a given API key.
        """
        if not api_key:
            raise ValueError("API Key cannot be empty.")
        self.api_key = api_key

    def get_user_profile(self, user_id: str) -> dict:
        """
        Fetches a user's profile information from the backend.
        
        Args:
            user_id: The unique identifier of the user.
            
        Returns:
            A dictionary containing the user's profile data.
            
        Raises:
            ValueError: If the user ID is invalid or the API key is invalid.
        """
        if not user_id:
            raise ValueError("User ID cannot be empty.")
        
        # Simulate API call using the stored key
        if self.api_key != "VALID_API_KEY":
            raise ValueError("Invalid API Key provided.")
            
        # Simulate fetching data
        if user_id == "user123":
            return {
                "user_id": user_id,
                "username": "jdoe",
                "email": "jdoe@example.com",
                "join_date": "2023-01-15",
                "status": "active"
            }
        elif user_id == "user456":
            return {
                "user_id": user_id,
                "username": "asmith",
                "email": "asmith@example.com",
                "join_date": "2022-11-01",
                "status": "inactive"
            }
        else:
            raise ValueError(f"User with ID {user_id} not found.")

    def process_data_request(self, data: dict) -> dict:
        """
        Processes a complex data request, simulating backend computation.
        
        Args:
            data: A dictionary containing the data payload.
            
        Returns:
            A dictionary containing the processed results.
            
        Raises:
            ValueError: If the data payload is missing required fields.
        """
        if not data or not isinstance(data, dict):
            raise ValueError("Data payload must be a non-empty dictionary.")
            
        required_fields = ["data_type", "payload"]
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
                
        # Simulate processing logic
        data_type = data["data_type"]
        payload = data["payload"]
        
        if data_type == "analysis":
            result = {"status": "success", "analysis_result": f"Analyzed {len(payload)} items."}
        elif data_type == "report":
            result = {"status": "success", "report_generated": True, "report_id": f"RPT-{hash(str(payload)) % 1000}"}
        else:
            result = {"status": "error", "message": f"Unsupported data type: {data_type}"}
            
        return result

# --- Test Cases (Self-Correction/Verification) ---
# print("--- Testing get_user_profile ---")
# try:
#     handler = ApiHandler("VALID_API_KEY")
#     profile = handler.get_user_profile("user123")
#     print(f"Success: {profile['username']}")
#     
#     profile_fail = handler.get_user_profile("unknown_user")
# except Exception as e:
#     print(f"Error caught (Expected): {e}")

# print("\n--- Testing process_data_request ---")
# try:
#     handler = ApiHandler("VALID_API_KEY")
#     data_payload = {"data_type": "analysis", "payload": [1, 2, 3]}
#     result = handler.process_data_request(data_payload)
#     print(f"Success: {result['status']}")
# except Exception as e:
#     print(f"Error caught (Expected): {e}")
