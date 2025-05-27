from dotenv import load_dotenv
import os

from langchain_openai import OpenAI
from langchain import hub
from langchain_community.utilities import SerpAPIWrapper
from langchain.tools import Tool
from langchain.agents import create_react_agent, AgentExecutor

# 환경 변수 로드
load_dotenv("key.env")

# API 키 가져오기
openai_api_key = os.getenv("OPENAI_API_KEY")
serpapi_api_key = os.getenv("SERPAPI_API_KEY")
langsmith_api_key = os.getenv("LANGSMITH_API_KEY")

# 프롬프트 가져오기
prompt = hub.pull("hwchase17/react")

# LLM 및 도구 준비
llm = OpenAI(openai_api_key=openai_api_key)
search = SerpAPIWrapper(serpapi_api_key=serpapi_api_key)
tools = [Tool(name="search", func=search.run, description="LLM이 관련 지식이 없을 때 지식 검색에 사용됩니다.")]

# 에이전트 및 실행기 생성
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 실행
print("첫 번째 실행 결과")
result = agent_executor.invoke({"input":"현재 인공지능 에이전트의 최신 연구 동향을 무엇입니까? 한글로 답해주세요!"})
print(result)
