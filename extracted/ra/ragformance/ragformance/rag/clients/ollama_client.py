import requests
import logging
import json

logging.basicConfig(level=logging.INFO)


class OllamaClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.headers: dict = {}  # You can set common headers here if needed

    def pull_model(self, model_name: str):
        """
        Télécharge/pull un modèle via Ollama, en gérant la réponse en streaming.
        """
        url = f"{self.base_url}/api/pull"

        payload = {"model": model_name, "stream": True}

        logging.info(
            f"Début de la requête de téléchargement pour le modèle {model_name} depuis {url}"
        )

        final_status = None

        try:
            with requests.post(
                url,
                headers={**self.headers, "Content-Type": "application/json"},
                json=payload,
                stream=True,
            ) as resp:
                resp.raise_for_status()

                logging.info(
                    f"Modèle {model_name} en cours de téléchargement (réception des données en streaming)..."
                )

                for line in resp.iter_lines():
                    if line:
                        try:
                            decoded_line = line.decode("utf-8")
                            json_response = json.loads(decoded_line)

                            status = json_response.get("status")
                            if status:
                                if (
                                    not final_status
                                    or final_status.get("status") != status
                                ):
                                    logging.info(f"  Statut ({model_name}): {status}")
                                    if (
                                        "total" in json_response
                                        and "completed" in json_response
                                    ):
                                        total = json_response["total"]
                                        completed = json_response["completed"]

                                        if total > 0:
                                            percentage = (completed / total) * 100
                                            logging.info(
                                                f"    Progression: {completed}/{total} ({percentage:.2f}%)"
                                            )
                            final_status = (
                                json_response  # Keep track of the last status
                            )

                        except Exception as e:
                            logging.error(
                                f"Erreur lors du traitement d'une ligne de la réponse: {e}"
                            )

            return (
                final_status
                if final_status
                else {"status": "completed with no detailed final status"}
            )

        except Exception as e:
            logging.error(
                f"Une erreur inattendue est survenue pendant le pull du modèle {model_name}: {e}"
            )
            raise

    def generate_response(self, model_name: str, prompt: str):
        """
        Generates a response from the specified Ollama model.
        This version is designed to be robust even if Ollama sends multiple
        JSON objects in the response when non-streaming is requested in the payload.
        It will return the last valid JSON object received.
        """
        url = f"{self.base_url}/api/generate"

        # Payload sent to Ollama: explicitly set stream to False.
        payload = {"model": model_name, "prompt": prompt, "stream": False}

        logging.info(
            f"Requesting text generation from model '{model_name}' at {url} (payload stream=False)"
        )

        last_json_response = None
        # To store the full raw response text for debugging if JSON parsing fails entirely
        raw_response_text_for_debugging = ""

        try:
            # Client-side streaming: Use stream=True in requests.post()
            # This allows us to iterate over lines even if Ollama sends multiple JSON objects.
            with requests.post(
                url,
                headers={
                    "Content-Type": "application/json"
                },  # Add any other common headers from self.headers
                json=payload,
                stream=True,  # Crucial: tells requests to stream the response body
            ) as response:
                response.raise_for_status()  # Check for HTTP errors (4xx, 5xx)

                for line in response.iter_lines():
                    if line:  # Filter out empty keep-alive newlines
                        decoded_line = line.decode("utf-8")
                        raw_response_text_for_debugging += decoded_line + "\n"
                        try:
                            # Attempt to parse the current line as a JSON object
                            current_json_part = json.loads(decoded_line)
                            # Store this part; if more parts come, this will be overwritten by the last one
                            last_json_response = current_json_part
                        except json.JSONDecodeError:
                            # Log if a specific line isn't valid JSON, but continue
                            # as other lines (especially the last one) might be the complete response.
                            logging.warning(
                                f"Could not decode a JSON line from stream: {decoded_line}"
                            )

                if not last_json_response:
                    # This means no line in the response was a valid JSON object.
                    logging.error(
                        f"No valid JSON object found in the response from '{model_name}'. "
                        f"Full raw response received:\n{raw_response_text_for_debugging}"
                    )
                    # Re-raise a more informative error or return an error structure
                    raise json.JSONDecodeError(
                        "No valid JSON object found in the entire response stream.",
                        raw_response_text_for_debugging,
                        0,
                    )

                # Correctly access the 'response' field from the parsed JSON for logging
                generated_text = last_json_response.get(
                    "response", "[No 'response' key in final JSON object]"
                )
                logging.info(
                    f"Generation from '{model_name}' complete. Response text snippet: {generated_text[:200]}..."
                )

                return last_json_response

        except Exception as e:
            # Catch any other unexpected errors
            logging.error(
                f"An unexpected error occurred during generation for model {model_name}: {e}"
            )
            raise
