# 환경 변수 설정: .env 파일에서 OPENAI_API_KEY, SERPAPI_API_KEY 등을 읽어옴
import os
from dotenv import load_dotenv

load_dotenv("../key.env")  # 상위 폴더의 key.env 파일에서 환경변수 로드

# LLM(대형 언어모델) 및 API 관련 설정
from openai import OpenAI
openai_api_key = os.getenv("OPENAI_API_KEY")  # OpenAI API 키
serpapi_api_key = os.getenv("SERPAPI_API_KEY")  # SerpAPI 키

# LangChain 관련 모듈 import
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain_community.utilities import SerpAPIWrapper
from langchain_experimental.tools.python.tool import PythonAstREPLTool

# LLM 인스턴스 생성
llm = ChatOpenAI(model="gpt-4", temperature=0)

# SerpAPI 기반의 구글 검색 도구 생성 (API 키 명시)
search = SerpAPIWrapper(serpapi_api_key=serpapi_api_key)

search_tool = Tool(
    name="Search",
    func=search.run,
    description="현재 정보를 검색하는 도구"
)

# LLM 기반 수학 계산을 위한 프롬프트 및 체인 구성
math_prompt = ChatPromptTemplate.from_messages([
    ("system", "Solve the math problem carefully."),
    ("user", "{question}")
])

# 파이프 연산자로 체인 구성 (Prompt -> LLM)
llm_math_chain = math_prompt | llm

# 수학 도구: 사용자 입력을 받아 LLM으로 계산 수행
math_tool = Tool(
    name="llm-math",
    func=lambda x: llm_math_chain.invoke({"question": x}).content,  # LLM 응답에서 content만 추출
    description="수학 문제를 해결하는 도구"
)

# 파이썬 코드 실행 도구
python_tool = PythonAstREPLTool()

# 사용할 도구 목록
tools = [search_tool, math_tool, python_tool]

# ReAct 프롬프트 템플릿 정의 (에이전트가 따라야 할 지침 및 형식 제공)
react_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a helpful AI agent that follows the ReAct framework.\n\n"
     "You can use the following tools:\n"
     "{tools}\n\n"
     "Use the following format:\n\n"
     "Question: the input question you must answer\n"
     "Thought: you should always think about what to do\n"
     "Action: the action to take, should be one of [{tool_names}]\n"
     "Action Input: the input to the action\n"
     "Observation: the result of the action\n"
     "... (this Thought/Action/Action Input/Observation can repeat N times)\n"
     "Thought: I now know the final answer\n"
     "Final Answer: the final answer to the original input question\n\n"
     "Begin!\n\n"
    ),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")  # 에이전트의 중간 기록 저장
])

# ReAct 에이전트 생성
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # Zero-shot ReAct 에이전트
    agent_kwargs={"prompt": react_prompt},
    verbose=True  # 실행 과정 출력
)

# 에이전트 실행: 질문 입력
input_question = (
    "현재 시장에서 장미의 일반적인 구매 가격은 얼마인가요?\n"
    "이 가격에 마진을 5%를 추가하려면 어떻게 가격을 책정해야 합니까?"
)

# 에이전트에 질문 전달 및 실행
result = agent.invoke({"input": input_question})

# 결과 출력
print(result["output"])

# 결과를 한국어로 출력하도록 유도하는 프롬프트 템플릿
react_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "최선을 다해 다음 질문에 답해 주세요."
     "능력이 부족할 경우, 아래 도구를 사용할 수 있습니다:\n\n"
     "You are a helpful AI agent that follows the ReAct framework.\n\n"
     "You can use the following tools:\n"
     "{tools}\n\n"
     "Use the following format:\n\n"
     "Question: the input question you must answer\n"
     "Thought: you should always think about what to do\n"
     "Action: the action to take, should be one of [{tool_names}]\n"
     "Action Input: the input to the action\n"
     "Observation: the result of the action\n"
     "... (this Thought/Action/Action Input/Observation can repeat N times)\n"
     "Thought: I now know the final answer\n"
     "Final Answer: the final answer to the original input question\n\n"
     "Begin!\n\n"
    ),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])