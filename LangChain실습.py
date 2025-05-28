# 환경 변수 설정
import os
from dotenv import load_dotenv

load_dotenv("key.env")

# 프롬프트 템플릿 설정
from langchain.prompts import PromptTemplate

prompt = PromptTemplate.from_template("{flower}의 꽃말은?")

# LLM 설정
from langchain_openai import OpenAI
openai_api_key = os.getenv("OPENAI_API_KEY")
model = OpenAI(api_key=openai_api_key)

# 출력 분석기 설정
from langchain.schema.output_parser import  StrOutputParser

output_parser = StrOutputParser()

# 연쇠 구성
chain = prompt | model | output_parser

# 연쇄를 실행하고 결과를 출력
result = chain.invoke({"flower": "라일락"})

print(result)
