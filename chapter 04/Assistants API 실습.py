# 환경 변수 설정
import os
from dotenv import load_dotenv

load_dotenv("../key.env")

# LLM 설정
from openai import OpenAI
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# 도우미 생성
assistant = client.beta.assistants.create(
    name="꽃 가격 계산기",
    instructions="당신은 제게 꽃의 가격을 계산해 줄 수 있습니다.",
    tools=[{"type":"code_interpreter"}],
    model="gpt-4o-mini"
)

# 도우미 출력
print(assistant)