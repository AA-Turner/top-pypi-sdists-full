import requests
import json
import string
import numpy as np


# TODO use litellm for LLM calls
def question_variation(
    question,
    nombre_variantes=5,
    API_KEY=None,
    API_URL="https://openrouter.ai/api/v1/chat/completions",
    API_MODEL="qwen/qwen3-32b:free",
):
    """
    Génère des variantes linguistiques d'une question donnée en utilisant l'API d'OpenRouter.
    La sortie est structurée en JSON pour faciliter la récupération automatique.
    """
    if not API_KEY:
        raise ValueError("Please set the API_KEY environment variable.")

    # TODO translate prompt to English
    prompt = (
        "Tu es un assistant expert en reformulation de questions.\n"
        "Ta tâche est de générer des reformulations linguistiques variées sur un lot de questions données sous la forme:\n"
        '{"_id": ID1, "query_text": QUESTION1}\n'
        '{"_id": ID2, "query_text": QUESTION2}\n'
        "...\n"
        "Conserve strictement le sens de la question initiale, tout en modifiant le style, la tournure ou le vocabulaire. Tu dois formuler des questions comme si un membre du grand public la formulait.\n"
        f'Voici la liste de questions : "{question}"\n\n'
        f"Génère exactement {nombre_variantes} variantes.\n"
        "Renvoie uniquement la réponse au format JSON suivant :\n"
        '{ID1: ["VARIATION1", "VARIATION2", "..."], ID2: ["VARIATION1", "VARIATION2", "..."]}'
    )

    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    payload = {
        "model": API_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "Tu es un assistant qui produit uniquement des réponses en format JSONL bien formé.",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.7,
    }

    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        message = response.json()["choices"][0]["message"]["content"].strip()

        # Tente de parser directement la réponse JSON
        message = json.loads(message)
        return message

    except Exception as e:
        print(f"Erreur lors de l'appel ou du parsing : {e}")
        return {}


# Write to JSONL
def generate_easy_question(tabular_data, category="None", tags=["None"], prefix_id=""):
    output, query_augmentation = [], []

    for idx, (error_code, (text, page_num)) in enumerate(tabular_data.items(), start=1):
        json_obj = {
            "_id": f"{prefix_id}_EASY_{idx}",
            "query_text": f"Que signifie le code d'erreur {error_code} ?",
            "relevant_document_ids": [
                {"corpus_id": f"DOC_{prefix_id}_p{page_num}", "score": 1}
            ],
            "ref_answer": text,  # Corrected typo from ref_anwser to ref_answer
            "metadata": {"category": category, "difficulty": "Easy", "tags": tags},
        }
        query_augmentation.append(
            {
                "_id": f"{prefix_id}_EASY_{idx}",
                "query_text": f"Que signifie le code d'erreur {error_code} ?",
            }
        )
        output.append(json_obj)

    return output, query_augmentation


def generate_med_question(
    tabular_data,
    document,
    category="None",
    tags=["None"],
    prefix_id="",
    API_KEY=None,
    API_URL="https://openrouter.ai/api/v1/chat/completions",
    API_MODEL="qwen/qwen3-32b:free",
):
    output, query_augmentation = [], []

    if not API_KEY:
        raise ValueError("Please set the API_KEY environment variable.")

    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    models = [
        API_MODEL,
    ]

    for idx, (error_code, (text, page_num)) in enumerate(tabular_data.items(), start=1):
        payload = {
            "models": models,
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "You are a text analysis assistant.\n"
                        f"Given the following troubleshoot, identify all the different step for solving the problem. For each step, extract the exact sentence or paragraph in which it appears, ensuring the text remains unaltered. Don't forget to add the page where the sentence has been extracted. Return the results in a JSON format includind all the step and it's associate page numbers.\n"
                        "Example output format:\n"
                        """{\n
                            "result": "1.EXTRACT_TEXT1 \n 2.EXTRACT_TEXT2 \n 3. ...",\n
                            "page": [PAGE1, PAGE2, ...],\n
                            ...\n
                            }\n"""
                        "where PAGE1 correspond to the page where EXTRACT_TEXT1 has been extracted, PAGE2 for EXTRACT_TEXT2, ...\n"
                        "The troubleshoot may not be indicated in the document. In this case, return an empty json (i.e., {})\n"
                        f"Troubleshoot to address: {text}\n\n"
                        f"Text to analyse: {document}"
                    ),
                }
            ],
        }

        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            response_json = response.json()
            message = response_json["choices"][0]["message"]["content"]
            print("Troubleshoot", text)
            print("Response", message)
            print()
            if message == "{}":
                continue

            message = json.loads(message)
            all_pages = message["page"]
            all_pages.append(page_num)
            json_obj = {
                "_id": f"{prefix_id}_MED_{idx}",
                "query_text": f"Quels sont les étapes pour résoudre le problème lié au code erreur {error_code} ?",
                "relevant_document_ids": [
                    {"corpus_id": f"DOC_{prefix_id}_p{i}", "score": 1}
                    for i in np.unique(all_pages)
                ],
                "ref_answer": message[
                    "result"
                ],  # Corrected typo from ref_anwser to ref_answer
                "metadata": {
                    "category": category,
                    "difficulty": "Medium",
                    "tags": tags,
                },
            }
            query_augmentation.append(
                {
                    "_id": f"{prefix_id}_MED_{idx}",
                    "query_text": f"Quels sont les étapes pour résoudre le problème lié au code erreur {error_code} ?",
                }
            )
            output.append(json_obj)
        else:
            print(f"Error during the request: {response.status_code}")
            print(response.text)
            continue
    return output, query_augmentation


# Supposons que `output` et `augmented_question` soient des chaînes de texte contenant du JSONL
# Exemple :
# output = '...'
# augmented_question = '...'
def add_augmented_question(main_data, variations_data):
    # Étape 2 : générer la liste finale d'objets
    final_entries = []

    for entry in main_data:
        base_id = entry["_id"]
        final_entries.append(entry)  # Ajouter la version principale

        # Ajouter les variations s'il y en a
        if base_id in variations_data:
            variations = variations_data[base_id]
            for idx, variation in enumerate(variations):
                letter = string.ascii_lowercase[idx]  # a, b, c, ...
                new_entry = entry.copy()
                new_entry["_id"] = f"{base_id}{letter}"
                new_entry["query_text"] = variation
                final_entries.append(new_entry)

    return final_entries
