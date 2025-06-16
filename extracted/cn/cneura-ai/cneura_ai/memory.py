import os
import re
import time
import hashlib
import json
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from pymongo import MongoClient
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from chromadb.api.types import EmbeddingFunction
from chromadb import HttpClient
from cneura_ai.logger import logger
from cneura_ai.llm import LLMInterface
from langchain.text_splitter import RecursiveCharacterTextSplitter

class GeminiEmbeddingFunction(EmbeddingFunction):
    def __init__(self, api_key: str):
        self.embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)

    def __call__(self, input: List[str]) -> List[List[float]]:
        return self.embedding_model.embed_documents(input)

class MemoryCollection:
    def __init__(self, HOST, PORT, namespace: str, name: str, gemini_api_key: str, chroma_token: str = None):
        # try:
        headers = {}
        if chroma_token:
                headers["Authorization"] = f"Bearer {chroma_token}"

        self.client = HttpClient(
                host=HOST,
                port=PORT,
                headers=headers
            )
        # except Exception as e:
        #     logger.error(f"Failed to connect to ChromaDB: {e}")
        #     raise

        self.model = GeminiEmbeddingFunction(api_key=gemini_api_key)
        self.namespace = namespace
        collection_name = f"{namespace}_{name}"
        self.content_hashes = set()

        existing_collections = [col.name for col in self.client.list_collections()]

        if collection_name in existing_collections:
            self.collection = self.client.get_collection(collection_name, embedding_function=self.model)
        else:
            self.collection = self.client.create_collection(collection_name, embedding_function=self.model, metadata={"hnsw:space": "cosine"})

    def get_content_hash(self, content: str) -> str:
        return hashlib.sha256(content.strip().encode()).hexdigest()
    
    def split_text(self, text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> List[str]:
        if len(text) <= chunk_size:
            return [text.strip()]
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        return splitter.split_text(text)

    def normalize(self, text: str) -> str:
        return re.sub(r'[^\w\s]', '', text.lower()).strip()

    async def store(self, key: str, memory: str, metadata: Optional[dict] = None):
        logger.info("Content chunking started.")
        chunks = self.split_text(memory)
        logger.info("Content chunking ended.")


        for i, chunk in enumerate(chunks):
            normalized_chunk = self.normalize(chunk)
            content_hash = self.get_content_hash(normalized_chunk)

            if content_hash in self.content_hashes:
                continue  # Skip duplicate chunks

            self.content_hashes.add(content_hash)

            chunk_id = f"{key}_chunk_{i}"
            chunk_metadata = {
                **(metadata or {}),
                "original_key": key,
                "chunk_index": i,
                "timestamp": time.time(),
                "content_hash": content_hash
            }
            logger.info(f"{chunk_id} - adding started.")
            self.collection.add(
                documents=[normalized_chunk],
                metadatas=[chunk_metadata],
                ids=[chunk_id]
            )
            logger.info(f"{chunk_id} - chunck added.")


    async def retrieve(self, query: str, top_k: int = 3, threshold: float = 0.85, use_similarity: bool = True) -> List[str]:
        query = self.normalize(query)

        results = self.collection.query(
            query_texts=[query],
            n_results=top_k,
            include=["documents", "distances"]
        )

        documents = []
        keys = []

        raw_distances = results["distances"][0]
        raw_documents = results["documents"][0]
        raw_ids = results["ids"][0]

        for i, distance in enumerate(raw_distances):
            similarity = 1.0 - distance if use_similarity else None

            if use_similarity:
                logger.info(f"[Similarity Filter] Distance: {distance:.4f}, Similarity: {similarity:.4f}")
                if similarity >= threshold:
                    documents.append(raw_documents[i])
                    keys.append(raw_ids[i])
            else:
                logger.info(f"[Distance Filter] Distance: {distance:.4f}")
                if distance <= threshold:
                    documents.append(raw_documents[i])
                    keys.append(raw_ids[i])

        logger.info(f"Retrieved documents (filter: {'similarity' if use_similarity else 'distance'} >= {threshold}): {documents}")
        logger.info(f"Retrieved keys: {keys}")

        return documents, keys

    async def delete(self, keys: List[str]):
        self.collection.delete(ids=keys)

    async def delete_all(self):
        all_ids = self.collection.get()["ids"]
        if all_ids:
            self.collection.delete(ids=all_ids)

class ShortTermMemory(MemoryCollection):
    def __init__(self, host, port, namespace: str, gemini_api_key: str, chroma_token: str = None, expiration_time: int = 60):
        super().__init__(host, port, namespace, "short_term_memory", gemini_api_key, chroma_token)
        self.expiration_time = expiration_time

    async def store(self, key: str, content: str):
        await super().store(key, content, metadata={'expiration_time': self.expiration_time})

    async def clean_up_expired(self):
        current_time = time.time()
        items = self.collection.get()
        expired_keys = []

        logger.info(f"Metadata items: {items['metadatas']}")
        for meta in items['metadatas']:
            key = meta.get('key')
            if key is None:
                continue  # or log a warning

            timestamp = meta.get('timestamp')
            expiration_time = meta.get('expiration_time', self.expiration_time)
            if timestamp and (current_time - timestamp > expiration_time):
                expired_keys.append(key)


        if expired_keys:
            await self.delete(expired_keys)
            logger.info(f"Removed expired STM entries from {self.namespace}: {expired_keys}")


class LongTermMemory(MemoryCollection):
    def __init__(self, host, port, namespace: str,gemini_api_key: str, chroma_token: str = None):
        super().__init__(host, port, namespace, "long_term_memory",gemini_api_key, chroma_token)


class KnowledgeBase(MemoryCollection):
    def __init__(self, host, port, namespace: str, gemini_api_key: str, chroma_token: str = None):
        super().__init__(host, port, namespace, "knowledge_base", gemini_api_key, chroma_token)


class AbilitiesMemory(MemoryCollection):
    def __init__(self, host, port, namespace: str, gemini_api_key: str, chroma_token: str = None):
        super().__init__(host, port, namespace, "abilities_memory", gemini_api_key, chroma_token)

class AgentsMemory(MemoryCollection):
    def __init__(self, host, port, namespace: str, gemini_api_key: str, chroma_token: str = None):
        super().__init__(host, port, namespace, "agents_memory", gemini_api_key, chroma_token)


class MemoryManager:
    def __init__(self, host, port, llm: LLMInterface, gemini_api_key: str, chroma_token: str = None):
        self.host = host
        self.port = port
        self.llm = llm
        self.gemini_api_key = gemini_api_key
        self.chroma_token = chroma_token
        self.namespaces = {}

    def get_namespace(self, namespace: str, expiration_time: int = 60):
        if namespace not in self.namespaces:
            self.namespaces[namespace] = {
                "long_term_memory": LongTermMemory(self.host, self.port, namespace, self.gemini_api_key, self.chroma_token),
                "short_term_memory": ShortTermMemory(self.host, self.port, namespace, self.gemini_api_key, self.chroma_token, expiration_time),
                "knowledge_base": KnowledgeBase(self.host, self.port, namespace, self.gemini_api_key, self.chroma_token),
                "abilities_memory": AbilitiesMemory(self.host, self.port, namespace, self.gemini_api_key, self.chroma_token),
                "agents_memory": AgentsMemory(self.host, self.port, namespace, self.gemini_api_key, self.chroma_token)
            }
        return self.namespaces[namespace]

    async def store_to_short_term(self, namespace: str, key: str, content: str):
        await self.get_namespace(namespace)["short_term_memory"].store(key, content)

    async def store_to_long_term(self, namespace: str, key: str, content: str):
        await self.get_namespace(namespace)["long_term_memory"].store(key, content)

    async def store_to_knowledge_base(self, namespace: str, key: str, content: str):
        await self.get_namespace(namespace)["knowledge_base"].store(key, content)

    async def store_to_abilities(self, namespace: str, key: str, content: str):
        await self.get_namespace(namespace)["abilities_memory"].store(key, content)

    async def store_in_namespace(self, namespace: str, content: str, key: str):
        decision_prompt = f"""
        Analyze the following content and classify it into one of these categories:
        - short_term_memory (temporary details, tasks)
        - long_term_memory (important facts)

        Content: {content}
        """
        schema = {
            "memory_type":{"description": "type of the memory. short_term_memory,long_term_memory", "optional": False},
            "memory": {"description":"The formatted, restructured and summarized memory. Include all important facts.", "optional": False}
        }

        try:
            response_text = self.llm.query(decision_prompt, schema)
            if not response_text.get("success", False):
                raise ValueError(response_text.get("error", "LLM ERROR"))
                
            data = response_text.get("data", None)
            if not data:
                raise ValueError("The data key not found on llm response")
            memory_type = data.get("memory_type")
            memory = data.get("memory", "")

            if memory_type not in ["short_term_memory", "long_term_memory"]:
                raise ValueError("Invalid memory type classified by LLM.")

        except Exception as e:
            logger.error(f"Failed to process LLM response: {e}")
            memory_type = "short_term_memory"
            memory = content

        logger.info(f"Classified memory type: {memory_type}, {memory}")

        memory_collection = self.get_namespace(namespace).get(memory_type)
        if memory_collection:
            await memory_collection.store(key, memory)
        else:
            logger.error(f"Invalid memory type: {memory_type}")

    async def retrieve_from_namespace(self, namespace: str, memory_type: str, query: str, top_k: int = 3) -> List[str]:
        memory_collection = self.get_namespace(namespace).get(memory_type)
        if memory_collection:
            return await memory_collection.retrieve(query, top_k)
        else:
            logger.error(f"Invalid memory type: {memory_type}")
            return []

    async def clean_up_namespace(self, namespace: str):
        short_term_memory = self.get_namespace(namespace)["short_term_memory"]
        await short_term_memory.clean_up_expired()

    async def delete_namespace(self, namespace: str):
        if namespace in self.namespaces:
            for memory_type in self.namespaces[namespace].values():
                await memory_type.delete_all()
            del self.namespaces[namespace]
            logger.info(f"Namespace {namespace} deleted.")

    async def retrieve_relevant_context(self, namespace: str, query: str, top_k_per_type: int = 2) -> Dict[str, List[str]]:
        relevant_context = {}
        memory_types = ["short_term_memory", "long_term_memory", "knowledge_base", "abilities_memory"]

        for mem_type in memory_types:
            try:
                documents = await self.retrieve_from_namespace(namespace, mem_type, query, top_k_per_type)
                if documents:
                    relevant_context[mem_type] = documents
            except Exception as e:
                logger.error(f"Failed to retrieve from {mem_type}: {e}")

        return relevant_context
    
    async def get_combined_context(self, namespace: str, query: str, top_k_per_type: int = 2) -> str:
        context = await self.retrieve_relevant_context(namespace, query, top_k_per_type)
        combined = ""

        for mem_type, entries in context.items():
            combined += f"\n[{mem_type.upper()}]\n"
            for entry in entries:
                if isinstance(entry, list): 
                    for sub_entry in entry:
                        combined += f"- {sub_entry.strip()}\n"
                else:
                    combined += f"- {entry.strip()}\n"

        return combined.strip()


class PersistentWorkingMemory:
    def __init__(self, mongo_uri, db_name="agent_db", collection_name="working_memory"):
        try:
            self.client = MongoClient(mongo_uri)
            self.db = self.client[db_name]
            self.collection = self.db[collection_name]
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    def _generate_slot_id(self):
        return f"slot_{uuid.uuid4()}"

    def _generate_state_id(self):
        return f"state_{uuid.uuid4()}"

    def _serialize_memory(self, memory):
        return json.dumps(memory, default=str)

    def _deserialize_memory(self, memory):
        return json.loads(memory)

    def save_memory(self, memory_slots):
        state_id = self._generate_state_id()
        memory_data = {
            "state_id": state_id,
            "timestamp": datetime.now(timezone.utc),
            "memory_slots": memory_slots
        }
        memory_data["serialized"] = self._serialize_memory(memory_data["memory_slots"])

        self.collection.insert_one(memory_data)
        return state_id

    def load_memory_by_state_id(self, state_id):
        result = self.collection.find_one({"state_id": state_id})
        if result:
            return self._deserialize_memory(result["serialized"])
        return None

    def update_memory(self, state_id, memory_slots):
        memory_data = {
            "timestamp": datetime.now(timezone.utc),
            "memory_slots": memory_slots,
            "serialized": self._serialize_memory(memory_slots)
        }
        result = self.collection.update_one(
            {"state_id": state_id},
            {"$set": memory_data},
            upsert=True
        )
        return result.modified_count

    def load_conversation_by_state_id(self, state_id):
        """Load a past conversation using its state ID."""
        result = self.collection.find_one({"state_id": state_id})
        print(result)
        if result and "serialized" in result:
            try:
                memory_slots = self._deserialize_memory(result["serialized"])
                conversation = [
                    {"role": slot.get("role"), "content": slot.get("content")}
                    for slot in memory_slots
                    if "role" in slot and "content" in slot
                ]
                return conversation
            except Exception as e:
                logger.error(f"Failed to deserialize memory: {e}")
                return []
        return []
