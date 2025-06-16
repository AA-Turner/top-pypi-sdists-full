import logging
from tqdm import tqdm
from typing import List, Dict
import uuid
import pandas as pd

from ragformance.rag.rag_interface import RagInterface
from ragformance.models.corpus import DocModel
from ragformance.models.answer import AnnotatedQueryModel, AnswerModel

from ragformance.rag.clients.ollama_client import OllamaClient
from ragformance.rag.clients.openwebui_client import OpenWebUIClient
from ragformance.rag.config import OpenWebUIRagConfig


logging.basicConfig(level=logging.INFO)


# SETUP

# Run the following docker command
# docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
# docker run -d -p 3000:8080 --gpus all --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:cuda

# You need to create an OpenWebUi user, either with the web Interface or with python
# With python :
# client = OpenWebUIClient(client_url)
# new_admin = client.create_user(
#    name="Admin user",
#    email="admin@example.com",
#    password="admin",
#    role="admin"
# )

# Add the email and password on the config file


class OpenwebuiRag(RagInterface):
    def __init__(self, config: OpenWebUIRagConfig):
        self.config = config
        # Ensure OLLAMA_URL and OPENWEBUI_URL are set if critical, or handle None
        if not self.config.OLLAMA_URL:
            logger.warning("OLLAMA_URL is not set in OpenWebUIRagConfig.")
        if not self.config.OPENWEBUI_URL:
            logger.warning("OPENWEBUI_URL is not set in OpenWebUIRagConfig.")

    def upload_corpus(self, corpus: List[DocModel]): # Removed config: Dict
        try:
            id_column = "id" # This could be made configurable if needed
            content_column = "text" # This could be made configurable if needed

            # Accessing configuration from self.config
            model_name = self.config.LLM_NAME
            collection_name = self.config.COLLECTION_NAME
            client_email = self.config.CLIENT_EMAIL
            client_mdp = self.config.CLIENT_MDP
            client_url = self.config.OPENWEBUI_URL
            
            if not client_url:
                 raise ValueError("OPENWEBUI_URL is not configured.")


            client = OpenWebUIClient(client_url)
            client.sign_in(client_email, client_mdp)

            coll_info = None

            logging.info(
                f"Début du benchmark sur la collection {collection_name} avec le modèle '{model_name}'."
            )
            # Ensure model_name is provided if it's critical for collection creation or logging
            if not model_name:
                logger.warning("LLM_NAME is not set, proceeding with collection creation.")


            coll_info = client.create_collection(
                name=collection_name,
                description="Collection pour benchmark", # This could be made configurable
            )

            if not coll_info or "id" not in coll_info:
                logging.error(
                    f"Échec de la création ou de la récupération de la collection '{collection_name}'."
                )
                return 0 # Return processed count as 0 or raise error

            collection_id = coll_info["id"]
            self.config.COLLECTION_ID = collection_id # Store collection_id in the config object
            logging.info(f"Utilisation de la collection ID: {collection_id}")

            df = pd.DataFrame([c.model_dump(by_alias=True) for c in corpus])

            add_results = client.add_documents_from_df_to_collection(
                df=df,
                collection_id=collection_id,
                doc_id_column=id_column,
                content_column=content_column,
            )

            logging.info(f"Résultats de l'ajout des documents du CSV: {add_results}")
            
            processed_count = add_results.get("processed_count", 0)
            return processed_count

        except Exception as e:
            logging.error(
                f"Une erreur est survenue durant l'upload du corpus: {e}", exc_info=True
            )
            raise e

    def ask_queries(self, queries: List[AnnotatedQueryModel]): # Removed config: Dict
        content_column = "query_text" # This could be made configurable if needed

        # Accessing configuration from self.config
        collection_id = self.config.COLLECTION_ID
        client_email = self.config.CLIENT_EMAIL
        client_mdp = self.config.CLIENT_MDP
        client_url = self.config.OPENWEBUI_URL
        ollama_url = self.config.OLLAMA_URL
        model_name = self.config.LLM_NAME

        if not client_url:
            raise ValueError("OPENWEBUI_URL is not configured.")
        if not ollama_url:
            # Decide if this is a fatal error or if it can proceed without ollama features
            logger.warning("OLLAMA_URL is not configured. Some functionalities might be affected.")
        if not collection_id:
            raise ValueError("COLLECTION_ID is not set. Please upload corpus first.")
        if not model_name:
            raise ValueError("LLM_NAME is not configured.")


        client = OpenWebUIClient(client_url)
        ollama_client = OllamaClient(ollama_url) # Handles None ollama_url gracefully if designed to

        client.sign_in(client_email, client_mdp)
        
        # Ensure model_name is available before pulling
        if ollama_url: # Only pull if ollama_url is set
             ollama_client.pull_model(model_name)


        answers = []
        df_queries = pd.DataFrame([c.model_dump(by_alias=True) for c in queries])

        try:
            for i, (df_index, row) in enumerate(
                tqdm(
                    df_queries.iterrows(),
                    total=df_queries.shape[0],
                    desc=f"Benchmarking ({model_name})",
                )
            ):
                query_text = row[content_column]

                raw_chat_output = client.chat_with_collection(
                    model_name, query_text, collection_id
                )

                model_answer_text, sourced_documents = client.parse_chat_response(
                    raw_chat_output
                )

                docs_retrieved = []
                docs_dist = []
                for doc in sourced_documents:
                    docs_retrieved.append(doc.get("name"))
                    docs_dist.append(doc.get("distance"))

                query = row.to_dict()
                answer = AnswerModel.model_validate(
                    {
                        "_id": str(uuid.uuid4()),
                        "query": query,
                        "model_answer": model_answer_text,
                        "retrieved_documents_ids": docs_retrieved,
                        "retrieved_documents_distances": docs_dist,
                    }
                )
                answers.append(answer)

            logging.info("Benchmark terminé.")
            client.delete_collection(collection_id)

        except Exception as e:
            logging.error(
                f"Une erreur est survenue durant le benchmark: {e}", exc_info=True
            )

        return answers
