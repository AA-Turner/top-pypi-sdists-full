import os
from uuid import uuid4

# from dotenv import load_dotenv
from flask import request, jsonify, Blueprint
from openai import AzureOpenAI
from ..batch.utilities.chat_history.auth_utils import (
    get_authenticated_user_details,
)
from ..batch.utilities.helpers.config.config_helper import ConfigHelper
from ..batch.utilities.helpers.env_helper import EnvHelper
from ..batch.utilities.chat_history.database_factory import DatabaseFactory
from mgmt_config import logger
# load_dotenv()

bp_chat_history_response = Blueprint("chat_history", __name__)

env_helper: EnvHelper = EnvHelper()
log_execution = env_helper.LOG_EXECUTION
log_args = env_helper.LOG_ARGS
log_result = env_helper.LOG_RESULT

@logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=log_result)
def init_database_client():
    try:
        conversation_client = DatabaseFactory.get_conversation_client()
        return conversation_client
    except Exception as e:
        logger.exception("Exception in database initialization: %s", e)
        raise e

@logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=log_result)
def init_openai_client():
    try:
        if env_helper.AZURE_AUTH_TYPE == "keys":
            azure_openai_client = AzureOpenAI(
                azure_endpoint=env_helper.AZURE_OPENAI_ENDPOINT,
                api_version=env_helper.AZURE_OPENAI_API_VERSION,
                api_key=env_helper.AZURE_OPENAI_API_KEY,
            )
        else:
            azure_openai_client = AzureOpenAI(
                azure_endpoint=env_helper.AZURE_OPENAI_ENDPOINT,
                api_version=env_helper.AZURE_OPENAI_API_VERSION,
                azure_ad_token_provider=env_helper.AZURE_TOKEN_PROVIDER,
            )
        return azure_openai_client
    except Exception as e:
        logger.exception("Exception in Azure OpenAI initialization: %s", e)
        raise e


@bp_chat_history_response.route("/history/list", methods=["GET"])
@logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=log_result)
def list_conversations():
    config = ConfigHelper.get_active_config_or_default()
    if not config.enable_chat_history:
        return jsonify({"error": "Chat history is not available"}), 400

    try:
        offset = request.args.get("offset", 0)
        authenticated_user = get_authenticated_user_details(
            request_headers=request.headers
        )
        user_id = authenticated_user["user_principal_id"]
        
        conversation_client = init_database_client()
        if not conversation_client:
            return jsonify({"error": "Database not available"}), 500

        conversation_client.connect()
        try:
            conversations = conversation_client.get_conversations(
                user_id, offset=offset, limit=25
            )
            if not isinstance(conversations, list):
                return (
                    jsonify({"error": f"No conversations for {user_id} were found"}),
                    404,
                )

            return jsonify(conversations), 200
        except Exception as e:
            logger.exception(f"Error fetching conversations: {e}")
            raise
        finally:
            conversation_client.close()

    except Exception as e:
        logger.exception(f"Exception in /history/list: {e}")
        return jsonify({"error": "Error while listing historical conversations"}), 500


@bp_chat_history_response.route("/history/rename", methods=["POST"])
@logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=log_result)
def rename_conversation():
    config = ConfigHelper.get_active_config_or_default()
    if not config.enable_chat_history:
        return jsonify({"error": "Chat history is not available"}), 400

    try:
        authenticated_user = get_authenticated_user_details(
            request_headers=request.headers
        )
        user_id = authenticated_user["user_principal_id"]

        # check request for conversation_id
        request_json = request.get_json()
        conversation_id = request_json.get("conversation_id", None)

        if not conversation_id:
            return (jsonify({"error": "conversation_id is required"}), 400)

        title = request_json.get("title", None)
        if not title or title.strip() == "":
            return jsonify({"error": "A non-empty title is required"}), 400

        # Initialize and connect to the database client
        conversation_client = init_database_client()
        if not conversation_client:
            return jsonify({"error": "Database not available"}), 500

        conversation_client.connect()
        try:
            # Retrieve conversation from database
            conversation = conversation_client.get_conversation(
                user_id, conversation_id
            )
            if not conversation:
                return (
                    jsonify(
                        {
                            "error": f"Conversation {conversation_id} was not found. It either does not exist or the logged in user does not have access to it."
                        }
                    ),
                    400,
                )

            # Update the title and save changes
            conversation["title"] = title
            updated_conversation = conversation_client.upsert_conversation(
                conversation
            )
            return jsonify(updated_conversation), 200
        except Exception as e:
            logger.exception(
                f"Error updating conversation: user_id={user_id}, conversation_id={conversation_id}, error={e}"
            )
            raise
        finally:
            conversation_client.close()
    except Exception as e:
        logger.exception(f"Exception in /history/rename: {e}")
        return jsonify({"error": "Error while renaming conversation"}), 500


@bp_chat_history_response.route("/history/read", methods=["POST"])
@logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=log_result)
def get_conversation():
    config = ConfigHelper.get_active_config_or_default()
    if not config.enable_chat_history:
        return jsonify({"error": "Chat history is not available"}), 400

    try:
        authenticated_user = get_authenticated_user_details(
            request_headers=request.headers
        )
        user_id = authenticated_user["user_principal_id"]

        # check request for conversation_id
        request_json = request.get_json()
        conversation_id = request_json.get("conversation_id", None)
        if not conversation_id:
            return jsonify({"error": "conversation_id is required"}), 400

        # Initialize and connect to the database client
        conversation_client = init_database_client()
        if not conversation_client:
            return jsonify({"error": "Database not available"}), 500

        conversation_client.connect()
        try:
            # Retrieve conversation
            conversation = conversation_client.get_conversation(
                user_id, conversation_id
            )
            if not conversation:
                return (
                    jsonify(
                        {
                            "error": f"Conversation {conversation_id} was not found. It either does not exist or the logged in user does not have access to it."
                        }
                    ),
                    400,
                )

            # Fetch conversation messages
            conversation_messages = conversation_client.get_messages(
                user_id, conversation_id
            )
            messages = [
                {
                    "id": msg["id"],
                    "role": msg["role"],
                    "content": msg["content"],
                    "createdAt": msg["createdAt"],
                    "feedback": msg.get("feedback"),
                }
                for msg in conversation_messages
            ]

            # Return formatted conversation and messages
            return (
                jsonify({"conversation_id": conversation_id, "messages": messages}),
                200,
            )
        except Exception as e:
            logger.exception(
                f"Error fetching conversation or messages: user_id={user_id}, conversation_id={conversation_id}, error={e}"
            )
            raise
        finally:
            conversation_client.close()

    except Exception as e:
        logger.exception(f"Exception in /history/read: {e}")
        return jsonify({"error": "Error while fetching conversation history"}), 500


@bp_chat_history_response.route("/history/delete", methods=["DELETE"])
@logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=log_result)
def delete_conversation():
    config = ConfigHelper.get_active_config_or_default()
    if not config.enable_chat_history:
        return jsonify({"error": "Chat history is not available"}), 400

    try:
        authenticated_user = get_authenticated_user_details(
            request_headers=request.headers
        )
        user_id = authenticated_user["user_principal_id"]

        # check request for conversation_id
        request_json = request.get_json()
        conversation_id = request_json.get("conversation_id", None)
        if not conversation_id:
            return jsonify({"error": "conversation_id is required"}), 400

        # Initialize and connect to the database client
        conversation_client = init_database_client()
        if not conversation_client:
            return jsonify({"error": "Database not available"}), 500

        conversation_client.connect()
        try:
            # Delete conversation and messages
            conversation_client.delete_conversation(user_id, conversation_id)
            conversation_client.delete_messages(conversation_id, user_id)
            return jsonify({"message": "Conversation deleted successfully"}), 200
        except Exception as e:
            logger.exception(
                f"Error deleting conversation: user_id={user_id}, conversation_id={conversation_id}, error={e}"
            )
            raise
        finally:
            conversation_client.close()
    except Exception as e:
        logger.exception(f"Exception in /history/delete: {e}")
        return jsonify({"error": "Error while deleting conversation"}), 500


@bp_chat_history_response.route("/history/delete_all", methods=["DELETE"])
@logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=log_result)
def delete_all_conversations():
    config = ConfigHelper.get_active_config_or_default()
    if not config.enable_chat_history:
        return jsonify({"error": "Chat history is not available"}), 400

    try:
        authenticated_user = get_authenticated_user_details(
            request_headers=request.headers
        )
        user_id = authenticated_user["user_principal_id"]

        # Initialize and connect to the database client
        conversation_client = init_database_client()
        if not conversation_client:
            return jsonify({"error": "Database not available"}), 500

        conversation_client.connect()
        try:
            # Get all conversations for the user
            conversations = conversation_client.get_conversations(user_id)
            if not isinstance(conversations, list):
                return jsonify({"error": "No conversations found"}), 404

            # Delete all conversations and messages
            for conversation in conversations:
                conversation_id = conversation["conversation_id"]
                conversation_client.delete_conversation(user_id, conversation_id)
                conversation_client.delete_messages(conversation_id, user_id)

            return jsonify({"message": "All conversations deleted successfully"}), 200
        except Exception as e:
            logger.exception(f"Error deleting all conversations: user_id={user_id}, error={e}")
            raise
        finally:
            conversation_client.close()
    except Exception as e:
        logger.exception(f"Exception in /history/delete_all: {e}")
        return jsonify({"error": "Error while deleting all conversations"}), 500


@bp_chat_history_response.route("/history/update", methods=["POST"])
@logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=log_result)
def update_conversation():
    config = ConfigHelper.get_active_config_or_default()
    if not config.enable_chat_history:
        return jsonify({"error": "Chat history is not available"}), 400

    try:
        authenticated_user = get_authenticated_user_details(
            request_headers=request.headers
        )
        user_id = authenticated_user["user_principal_id"]

        # check request for conversation_id
        request_json = request.get_json()
        conversation_id = request_json.get("conversation_id", None)
        if not conversation_id:
            return jsonify({"error": "conversation_id is required"}), 400

        # Initialize and connect to the database client
        conversation_client = init_database_client()
        if not conversation_client:
            return jsonify({"error": "Database not available"}), 500

        conversation_client.connect()
        try:
            # Retrieve conversation from database
            conversation = conversation_client.get_conversation(
                user_id, conversation_id
            )
            if not conversation:
                return (
                    jsonify(
                        {
                            "error": f"Conversation {conversation_id} was not found. It either does not exist or the logged in user does not have access to it."
                        }
                    ),
                    400,
                )

            # Update conversation with new data
            conversation.update(request_json)
            updated_conversation = conversation_client.upsert_conversation(
                conversation
            )
            return jsonify(updated_conversation), 200
        except Exception as e:
            logger.exception(
                f"Error updating conversation: user_id={user_id}, conversation_id={conversation_id}, error={e}"
            )
            raise
        finally:
            conversation_client.close()
    except Exception as e:
        logger.exception(f"Exception in /history/update: {e}")
        return jsonify({"error": "Error while updating conversation"}), 500


@bp_chat_history_response.route("/history/frontend_settings", methods=["GET"])
@logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=log_result)
def get_frontend_settings():
    config = ConfigHelper.get_active_config_or_default()
    return jsonify({
        "enable_chat_history": config.enable_chat_history,
        "max_conversations": 25,
        "max_messages_per_conversation": 100
    })


def generate_title(conversation_messages):
    """Generate a title for a conversation based on its messages."""
    if not conversation_messages:
        return "New Conversation"
    
    # Get the first user message
    for message in conversation_messages:
        if message.get("role") == "user":
            content = message.get("content", "")
            # Truncate to 50 characters and clean up
            title = content[:50].strip()
            if len(content) > 50:
                title += "..."
            return title if title else "New Conversation"
    
    return "New Conversation"
