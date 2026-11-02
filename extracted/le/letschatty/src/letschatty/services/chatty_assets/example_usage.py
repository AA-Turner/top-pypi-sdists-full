"""
Example usage of the AssetsCollections class

This file demonstrates how to use the read-only AssetsCollections container
in a microservice.
"""
from .assets_collections import AssetsCollections
from ...models.data_base.mongo_connection import MongoConnection

# Example: How to use AssetsCollections in a microservice

def example_usage():
    """
    Example of how to use AssetsCollections in your microservice.
    """
    # Initialize the connection (typically this would be a singleton in your microservice)
    connection = MongoConnection()

    # Get the singleton instance
    assets = AssetsCollections(connection)

    # Read assets by ID
    # product = assets.get_product_by_id("some_product_id")
    # tag = assets.get_tag_by_id("some_tag_id")
    # user = assets.get_user_by_id("some_user_id")
    # chat = assets.get_chat_by_id("some_chat_id")
    # source = assets.get_source_by_id("some_source_id")
    # flow = assets.get_flow_by_id("some_flow_id")
    # sale = assets.get_sale_by_id("some_sale_id")
    # contact_point = assets.get_contact_point_by_id("some_contact_point_id")
    # ai_agent = assets.get_ai_agent_by_id("some_ai_agent_id")

    # Or access the collections directly for more advanced queries
    # all_products = assets.products.get_docs(query={"active": True}, company_id="some_company_id")

    print("AssetsCollections initialized and ready to use!")

    # Note: This is read-only. No insert, update, or delete operations are available.
    # For write operations, use the full AssetService classes in the API.


if __name__ == "__main__":
    example_usage()

