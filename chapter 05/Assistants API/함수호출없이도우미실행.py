# 환경 변수 설정
import os
from dotenv import load_dotenv
from openai.resources.beta import assistants

load_dotenv("../../key.env")

# LLM 설정
from openai import OpenAI
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# 생성한 도우미 획득
assistant_id = 'asst_KxvFRUVBMLRkKOrJZ3InxNHN'

# 새로운 대화 흐름 생성
thread = client.beta.threads.create()
print(f"대화 흐름 정보: \n{thread}\n")

# 대화 흐름에 사용자 메세지 추가
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="안녕하세요? 그냥 아무 말이나 해주세요!"
)

print(f"메세지 정보: \n{message}\n")

# 실행 세션을 생성하여 대화 흐름 처리
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant_id
)

print(f"실행 세션 초기 정보: \n{run}\n")

# 실행 세션 상태 확인
import time

n =0
while True:
    n += 1

    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )

    print(f"{n}번째 실행 세션 정보:\n{run}\n")

    if run.status == 'completed':
        break

    time.sleep(5)

# 대화 흐름에서 도우미 응답 가져오기
messages = client.beta.threads.messages.list(thread_id=thread.id)

# 도우미 응답 출력
for message in messages.data:
    if message.role == "assistant":
        print(f"도우미 응답: \n{message}\n")


