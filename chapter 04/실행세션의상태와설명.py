# 환경 변수 설정
import os
from dotenv import load_dotenv

load_dotenv("../key.env")

# LLM 설정
from openai import OpenAI
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# 대화 흐름과 도우미 ID 지정
thread_id = 'thread_hv2woQuHYgq1HSVzHwMPYeIA'
assistant_id = 'asst_8gZ9bWgrPZZaNauCbSDxnzMu'

# 실행 세션 생성
run = client.beta.threads.runs.create(
    thread_id= thread_id,
    assistant_id=assistant_id,
    instructions="질문에 답변해 주세요." # 여기서 새로운 지침을 설정할 수 있습니다.
)

# 확인 간격 시간 설정(5초)
polling_interval = 5

# 실행 세션 상태 확인 시작
import time

while True:
    run = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run.id,
    )

    # 실행 세션 객체의 속성에 직접 접근
    status = run.status

    print(f"Run status: {status}")

    # 실행 세션의 상태가 'completed', 'failed', 'expired'일 경우 순환 종료
    if status in ['completed', 'failed', 'expired']:
        break

    # 확인 간격 시간 대기 후 반복
    time.sleep(polling_interval)

# 실행 세션 결과 처리
if status == 'completed':
    print("성공!")


elif status in ['failed', 'expired']:
    print("실패")
