import json
import logging
from openai import OpenAI
import os
import sys
# from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from langchain import OpenAI as LangchainOpenAI
from langsmith import wrappers, traceable
from dotenv import load_dotenv
 
load_dotenv(verbose=True)
 
# app = FastAPI()
 
# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
 
# OpenAI 클라이언트 초기화
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)
 
def generate_questions(pipeline: dict, target: str, purpose: str, multipleChoiceCount: int, openEndedCount: int):
    """설문 문항을 생성하는 함수"""

    # # Langchain 체인 생성
    # model = ChatOpenAI(
    #     model_name="gpt-4o-mini",
    #     temperature=0.7,
    #     openai_api_key=os.getenv('OPENAI_API_KEY')
    # )
    # chain = prompt | model | StrOutputParser()

    # # 체인 실행
    # response = chain.invoke({})

    # return {
    #     'response': response,
    #     'artifact': None
    # }

   
def basic_analysis(question: str):
    """기본 설문 분석을 수행하는 함수"""
    #...
    #     logger.info(f"Successfully analyzed question: {question}")
    #     return {
    #         'response': analysis_response,
    #         "artifact": chart_data
    #     }
 
    # except Exception as e:
    #     logger.error(f"Error in basic analysis: {str(e)}")
    #     raise Exception(f"Failed to perform basic analysis: {str(e)}")
 