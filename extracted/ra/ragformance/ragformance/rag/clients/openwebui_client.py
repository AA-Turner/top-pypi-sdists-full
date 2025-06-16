import requests
import logging
import pandas as pd
import mimetypes
import os
import json
import tempfile
from tqdm import tqdm


logging.basicConfig(level=logging.INFO)


class OpenWebUIClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.token = (
            os.environ["OPENWEBUI_TOKEN"] if "OPENWEBUI_TOKEN" in os.environ else None
        )
        self.headers: dict = {}

        if self.token:
            self.headers = {"Authorization": f"Bearer {self.token}"}

    def sign_in(self, email: str, password: str):
        """
        Authentifie l’utilisateur et récupère un token JWT.
        Endpoint: POST /api/v1/auths/signin
        """
        url = f"{self.base_url}/api/v1/auths/signin"
        payload = {"email": email, "password": password}
        resp = requests.post(url, json=payload)
        resp.raise_for_status()
        self.token = resp.json().get("token")
        if not self.token:
            raise ValueError("Token non trouvé dans la réponse")
        self.headers = {"Authorization": f"Bearer {self.token}"}
        logging.info("Authentification réussie")

    def create_user(self, name: str, email: str, password: str, role: str = "admin"):
        url = f"{self.base_url}/api/v1/auths/signup"
        payload = {"name": name, "email": email, "password": password, "role": role}
        resp = requests.post(url, headers={**self.headers}, json=payload)
        resp.raise_for_status()
        logging.info(f"Utilisateur {email} créé")
        return resp.json()

    def create_collection(self, name: str, description: str = ""):
        """
        Crée une nouvelle collection de connaissance.
        Endpoint: POST /api/v1/knowledge/create
        """
        url = f"{self.base_url}/api/v1/knowledge/create"
        payload = {
            "name": name,
            "description": description,
            "data": {},
            "access_control": {},
        }
        resp = requests.post(url, headers={**self.headers}, json=payload)
        resp.raise_for_status()
        collection = resp.json()
        logging.info(f"Collection '{name}' créée (ID: {collection['id']})")
        return collection

    def upload_file(self, file_path: str):
        """
        Upload d’un fichier pour RAG.
        Endpoint: POST /api/v1/files/
        """
        url = f"{self.base_url}/api/v1/files/"
        # get the content_type
        filename = os.path.basename(file_path)
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            mime_type = "application/octet-stream"

        with open(file_path, "rb") as f:
            files = {"file": (filename, f, mime_type)}
            resp = requests.post(
                url,
                headers={**self.headers},
                files=files,
            )

        resp.raise_for_status()
        file_info = resp.json()
        # logging.info(f"Fichier {file_path} uploadé (ID: {file_info['id']})")
        return file_info

    def add_file_to_collection(self, collection_id: str, file_id: str):
        """
        Ajoute un fichier à une collection existante.
        Endpoint: POST /api/v1/knowledge/{id}/file/add
        """
        url = f"{self.base_url}/api/v1/knowledge/{collection_id}/file/add"
        payload = {"file_id": file_id}
        resp = requests.post(
            url,
            headers={**self.headers, "Content-Type": "application/json"},
            json=payload,
        )
        resp.raise_for_status()
        # logging.info(f"Fichier {file_id} ajouté à la collection {collection_id}")
        return resp.json()

    def delete_collection(self, collection_id: str):
        """
        Supprime une collection de connaissance.
        Endpoint: DELETE /api/v1/knowledge/{id}
        """
        url = f"{self.base_url}/api/v1/knowledge/{collection_id}/delete"
        try:
            resp = requests.delete(url, headers=self.headers)
            resp.raise_for_status()
            logging.info("Collection supprimée")
        except Exception as e:
            logging.error(f"Erreur lors de la suppréssion de la collection : {e}")
            raise

    def add_documents_from_df_to_collection(
        self,
        df: pd.DataFrame,
        collection_id: str,
        doc_id_column: str = "Doc_page_ID",
        content_column: str = "Content",
        file_extension: str = ".txt",
        encoding: str = "utf-8",
    ):
        """
        Lit un fichier CSV, crée des fichiers texte à partir de son contenu,
        les télécharge et les ajoute à une collection spécifiée.
        """

        if not self.token:
            logging.error("Client non authentifié. Veuillez d'abord appeler sign_in().")
            raise RuntimeError("Client non authentifié.")

        processed_count = 0
        failed_ids = []

        if doc_id_column not in list(df.columns.values) or content_column not in list(
            df.columns.values
        ):
            msg = (
                f"Les colonnes '{doc_id_column}' et/ou '{content_column}' sont "
                f"introuvables dans les en-têtes du DataFrame: {list(df.columns.values)}"
            )
            logging.error(msg)
            raise ValueError(msg)

        try:
            # Créer un répertoire temporaire pour stocker les fichiers avant l'upload
            with tempfile.TemporaryDirectory() as temp_dir:
                logging.info(f"Utilisation du répertoire temporaire : {temp_dir}")
                for i, row in tqdm(df.iterrows(), total=len(df)):
                    doc_page_id = row.get(doc_id_column)
                    content = row.get(content_column)

                    if not doc_page_id:
                        # logging.warning(f"Ligne {i+1}: '{doc_id_column}' est manquant ou vide. Ligne ignorée.")
                        failed_ids.append(f"Ligne {i+1} (ID manquant)")
                        continue
                    if (
                        content is None
                    ):  # Permettre un contenu vide, mais pas s'il est absent
                        # logging.warning(f"Ligne {i+1} (ID: {doc_page_id}): '{content_column}' est manquant. Ligne ignorée.")
                        failed_ids.append(doc_page_id)
                        continue

                    sane_filename_base = "".join(c for c in doc_page_id)
                    temp_filename = f"{sane_filename_base}{file_extension}"
                    temp_file_path = os.path.join(temp_dir, temp_filename)

                    try:
                        with open(temp_file_path, "w", encoding=encoding) as tmp_f:
                            tmp_f.write(content)
                        # logging.info(f"Fichier temporaire créé : {temp_file_path} pour Doc_page_ID '{doc_page_id}'")

                        # 1. Upload le fichier temporaire
                        file_info = self.upload_file(temp_file_path)
                        file_id = file_info["id"]
                        # logging.info(f"Doc ID '{doc_page_id}' (Fichier: {temp_filename}) uploadé avec succès. File ID serveur: {file_id}")

                        # 2. Ajoute le fichier uploadé à la collection
                        self.add_file_to_collection(collection_id, file_id)
                        # logging.info(f"Doc ID '{doc_page_id}' (File ID: {file_id}) ajouté à la collection {collection_id}")
                        processed_count += 1

                    except Exception:
                        # logging.error(f"Erreur lors du traitement du Doc_page_ID '{doc_page_id}': {e}")
                        failed_ids.append(doc_page_id)

        except Exception as e:
            logging.error(f"Erreur générale lors du traitement du DataFrame: {e}")
            raise
        finally:
            logging.info(
                f"Traitement du CSV terminé. {processed_count} documents ajoutés avec succès."
            )
            if failed_ids:
                logging.warning(
                    f"{len(failed_ids)} documents n'ont pas pu être traités : {failed_ids}"
                )

        return {"processed_count": processed_count, "failed_ids": failed_ids}

    def chat_with_collection(self, model: str, query: str, collection_id: str):
        """
        Lance une requête RAG en se basant sur une collection.
        Endpoint: POST /api/chat/completions
        """
        url = f"{self.base_url}/api/chat/completions"
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": query}],
            "files": [{"type": "collection", "id": collection_id}],
            "stream": True,
        }
        retrieved_sources = None
        final_answer = []
        try:
            with requests.post(
                url,
                headers={
                    **self.headers,
                    "Content-Type": "application/json",
                    "Accept": "text/event-stream",
                },
                json=payload,
                stream=True,  # Nécessaire pour obtenir les résultats du retrieval
            ) as resp:
                resp.raise_for_status()  # erreurs HTTP avant de lire le flux

                for line in resp.iter_lines():
                    if line:
                        decoded_line = line.decode("utf-8")

                        if decoded_line.startswith("data: "):
                            json_content_str = decoded_line[len("data: ") :]

                            if json_content_str == "[DONE]":
                                break

                            try:
                                chunk = json.loads(json_content_str)
                                # logging.debug(f"Chunk JSON: {chunk}")

                                if "sources" in chunk:
                                    retrieved_sources = chunk["sources"]
                                    # logging.info(f"Sources récupérées: {retrieved_sources}")

                                if "choices" in chunk and chunk["choices"]:
                                    delta = chunk["choices"][0].get("delta", {})
                                    content_part = delta.get("content")
                                    if content_part:
                                        final_answer.append(content_part)

                            except json.JSONDecodeError as e:
                                logging.error(
                                    f"Erreur de décodage JSON pour le chunk: '{json_content_str}'. Erreur: {e}"
                                )

        except Exception as e:
            logging.error(
                f"Erreur lors du traitement du flux de chat: {e}", exc_info=True
            )
            raise

        full_response_text = "".join(final_answer)
        # logging.info(f"Réponse finale assemblée: {full_response_text}")

        return {"sources": retrieved_sources, "answer": full_response_text}

    def parse_chat_response(self, chat_result: dict):
        if not isinstance(chat_result, dict):
            logging.error("L'entrée doit être un dictionnaire.")
            return None, []

        final_answer = chat_result.get("answer", "Réponse non trouvée.")
        sourced_documents = []

        sources_list = chat_result.get("sources")

        if sources_list and isinstance(sources_list, list) and len(sources_list) > 0:
            source_data_block = sources_list[0]
            if isinstance(source_data_block, dict):
                # documents_content = source_data_block.get('document', [])

                metadata_list = source_data_block.get("metadata", [])
                distances_list = source_data_block.get("distances", [])

                num_sources = min(len(metadata_list), len(distances_list))
                for i in range(num_sources):
                    doc_info = {}
                    metadata_item = metadata_list[i]

                    doc_info["name"] = metadata_item.get("name", "Nom inconnu")
                    # remove file extension
                    doc_info["name"] = doc_info["name"].replace(".txt", "")
                    doc_info["distance"] = distances_list[i]

                    sourced_documents.append(doc_info)
            else:
                logging.warning(
                    "Le premier élément de 'sources' n'est pas un dictionnaire."
                )

        elif sources_list is None:
            logging.info("Aucune clé 'sources' trouvée dans la réponse.")
        else:
            logging.warning(
                f"La clé 'sources' n'est pas une liste valide ou est vide: {sources_list}"
            )

        return final_answer, sourced_documents

    def get_rag_config(self):
        """
        Récupère la configuration du rag OpenWebUi
        Endpoint: GET /api/v1/retrieval/config
        """
        url = f"{self.base_url}/api/v1/retrieval/config"

        try:
            resp = requests.get(
                url, headers={**self.headers, "Content-Type": "application/json"}
            )
            resp.raise_for_status()
            return resp.json()

        except Exception as e:
            logging.error(
                f"Erreur lors de la récupération de la configuration OpenWebUi: {e}"
            )
            raise

    def update_rag_config(self, **config_updates):
        """
        Met à jour les configurations du système RAG OpenWebUI
        """
        url = f"{self.base_url}/api/v1/retrieval/config/update"

        request_headers = {**self.headers, "Content-Type": "application/json"}
        try:
            response = requests.post(url, headers=request_headers, json=config_updates)
            response.raise_for_status()
            updated_config = response.json()
            logging.info("Configuration mise à jour avec succès")

            return updated_config

        except Exception as e:
            logging.error(
                f"Erreur lors de la mise à jour de la configuration OpenWebUi: {e}"
            )
            raise
