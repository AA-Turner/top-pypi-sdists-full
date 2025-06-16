import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from cneura_ai.research import Research
from cneura_ai.llm import GeminiLLM
from cneura_ai.memory import MemoryManager
from cneura_ai.logger import logger
from app.dependencies import get_db_hub, DatabaseHub

router = APIRouter(prefix="/research", tags=["Research"])

class SearchRequest(BaseModel):
    agent_id: str
    query: str
    num_results: int = Field(default=1, ge=1, le=10)


async def get_memory_manager(db_hub: DatabaseHub = Depends(get_db_hub)) -> MemoryManager:
    await db_hub.load_config()
    gemini_api_key = db_hub.config.get("GEMINI_API_KEY")
    chroma_host = db_hub.config.get("CHROMA_HOST", "localhost")
    chroma_port = int(db_hub.config.get("CHROMA_PORT", 8888))
    chroma_token = db_hub.config.get("CHROMADB_API_KEY")

    llm_instance = GeminiLLM(api_key=gemini_api_key)

    return MemoryManager(host=chroma_host, port=chroma_port, llm=llm_instance, gemini_api_key=gemini_api_key, chroma_token=chroma_token)


async def get_research_instance(db_hub: DatabaseHub = Depends(get_db_hub)) -> Research:
    await db_hub.load_config()
    brave_api_key = db_hub.config.get("BRAVE_API_KEY")
    if not brave_api_key:
        raise HTTPException(status_code=500, detail="BRAVE_API_KEY is missing in DB config.")
    return Research(api_key=brave_api_key)


@router.post("/search")
async def search(
    request: SearchRequest,
    research_instance: Research = Depends(get_research_instance),
    memory_manager: MemoryManager = Depends(get_memory_manager),
):
    try:
        contents = research_instance.search_with_content(
            query=request.query,
            count=request.num_results
        )

        llm = memory_manager.llm  # Already constructed with Gemini API key
        summaries = []

        for content in contents:
            summarize_prompt = ("system", f"""
                You are a professional data analyst specializing in extracting key information and generating detailed, structured descriptions from web-scraped content.
                
                Given the user's query and the scraped content, your task is to produce a comprehensive, informative explanation that:
                - Directly addresses the user's intent.
                - Highlights all important points, facts, and insights.
                - Preserves the depth, structure, and nuance of the original content.
                - Avoids generalizations and includes specific, meaningful details.

                User Query: {request.query}

                Scrape result:
                - Title: {content.get("title")}
                - Description: {content.get("description")}
                - Content: {content.get("content").strip()}
            """)
            response = llm.query(summarize_prompt)

            if response.get("success", False):
                summaries.append(response.get("data"))
                logger.info("Content summarized")
            else:
                logger.error("Summarization failed: %s", response)

        merge_prompt = ("system", f"""
            You are a professional data analyst and content synthesizer.
            Your task is to merge the following detailed descriptions into a single, cohesive, and comprehensive explanation.

            Requirements:
            - Preserve all important facts, insights, and nuances from each description.
            - Eliminate redundancy while retaining clarity and depth.
            - Ensure the merged result is well-structured and logically coherent.
            - Do not simplify the content — maintain detailed and informative tone throughout.

            Detailed Descriptions:
            {summaries}
        """)

        response = llm.query(merge_prompt)

        if response.get("success", False):
            logger.info("Content merged")
            await memory_manager.store_to_knowledge_base(request.agent_id, str(uuid.uuid4()), response.get("data"))
            logger.info("Merged content added to Knowledge base")

            return JSONResponse(content={
                "status": "completed",
                "results": response.get("data")
            })
        else:
            logger.error("Merging failed: %s", response)
            return JSONResponse(content={
                "status": "failed",
                "error": "Merging LLM failed."
            }, status_code=500)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


