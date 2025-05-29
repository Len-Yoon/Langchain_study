# 환경 변수 설정
import os
from dotenv import load_dotenv

load_dotenv("../key.env")

# LLM 설정
from openai import OpenAI
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# 생성한 도우미 목록 얻기
assistants = client.beta.assistants.list()

# 대화 흐름 생성
thread = client.beta.threads.create()

# 대화 흐름에 메시지 추가
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="각 꽃다발의 가격을 원가에 20% 더한 가격으로 책정할려해요. 원가가 2000원일 때, 제 판매가격은 얼마인가요?"
)

# 메세지 출력
print(message)
