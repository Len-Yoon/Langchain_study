# 환경 변수 설정
import os
from dotenv import load_dotenv
from openai.resources.beta import assistants

load_dotenv("../../key.env")

# LLM 설정
from openai import OpenAI
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# 이전에 생성한 도우미 획득
assistant_id = 'asst_KxvFRUVBMLRkKOrJZ3InxNHN'
assistant = client.beta.assistants.retrieve(assistant_id)

# 새로운 대화 흐름 생성
thread = client.beta.threads.create()

print(f"대화 흐름 정보:\n{thread}\n")

# 대화 흐름에 사용자 메시지 추가
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="안녕하세요, 슬픈 예나를 위로해 주세요!"  # 변경 부분
)

print(f"메시지 정보:\n{message}\n")

# 실행 세션을 생성하여 대화 흐름 처리
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant_id
)

print(f"실행 세션 초기 정보:\n{run}\n")

import time

# 실행 세션 상태 확인 함수
def poll_run_status(client, thread_id, run_id, interval=5):
    n = 0

    while True:
        n += 1

        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)

        print(f"{n}번째 실행 세션 정보:\n{run}\n")

        if run.status in ['requires_action', 'completed']:
            return run

        time.sleep(interval)  # 일정 시간 대기 후 다시 상태 확인

# 실행 세션 상태 확인
run = poll_run_status(client, thread.id, run.id)

# 실행 세션에서 함수 속성 정보를 획득하는 함수
def get_function_details(run):
    function_name = run.required_action.submit_tool_outputs.tool_calls[0].function.name
    arguments = run.required_action.submit_tool_outputs.tool_calls[0].function.arguments
    function_id = run.required_action.submit_tool_outputs.tool_calls[0].id
    return function_name, arguments, function_id

# 함수 속성 정보 가져오가
function_name, arguments, function_id = get_function_details(run)

print("function_name:", function_name)
print("arguments:", arguments)
print("function_id:", function_id)

# 응원 메시지 함수
def get_encouragement(mood, name=None):
    # 응원 메시지
    messages = {
        "행복": "당신이 이렇게 밝게 웃고 있는 걸 보니 기분이 좋아요! 긍정적인 마음을 계속 유지하세요!",
        "슬픔": "기억하세요. 가장 어두운 구름 뒤에도 항상 햇살이 당신을 기다리고 있어요.",
        "피곤함": "당신은 이미 충분히 잘했어요. 이제 잠시 쉬어 갈 시간이예요.",
        "스트레스": "깊게 숨을 들이마시고, 천천히 내쉬세요. 모든 것이 잘 될 거예요."
    }

    # 기분에 맞는 응원 메시지 가져오기
    if name:
        message = f"{name}님, {messages.get(mood, '오늘 기분이 어떠신가요? 저는 항상 당신을 응원하고 있어요!')}"
    else:
        message = messages.get(mood, "오늘 기분이 어떠신가요? 저는 항상 당신을 응원하고 있어요!")

    # 맞춤형 응원 메시지 반환
    return message

# JSON 문자열을 사전으로 변환
import json

arguments_dict = json.loads(arguments)

# 사전에서 'name'과 'mood' 추출
name = arguments_dict['name']
mood = arguments_dict['mood']

# 함수 호출
encouragement_message = get_encouragement(mood, name)

# 결과 출력
print(encouragement_message)

# 동적 함수 호출을 위한 사전 정의
available_functions = {
    "get_encouragement": get_encouragement
}

# 매개 변수 처리
import json

function_args = json.loads(arguments)

# 동적 함수 호출
function_to_call = available_functions[function_name]
encouragement_message = function_to_call(
    name=function_args.get("name"),
    mood=function_args.get("mood")
)

# 결과 출력
print(encouragement_message)

# 결과 제출 함수
def submit_tool_outputs(run, thread, function_id, function_response):
    run = client.beta.threads.runs.submit_tool_outputs(
        thread_id=thread.id,
        run_id=run.id,
        tool_outputs=[
            {
                "tool_call_id": function_id,
                "output": str(function_response),
            }
        ]
    )

    return run

# 실행 세션에 결과 제출
run = submit_tool_outputs(run, thread, function_id, encouragement_message)

print('실행 세션이 결과를 받았습니다.')
print(run)

# 실행 세션 상태를 확인하여 완료될 때까지 대기
run = poll_run_status(client, thread.id, run.id)

print('실행 세션이 완료될 때까지 계속 실행됩니다.')
print(run)

# 대화 흐름에서 도우미의 응답 가져오기
messages = client.beta.threads.messages.list(thread_id=thread.id)

# 도우미의 응답 출력
print('최종 메시지 출력:')
for message in messages.data:
    if message.role == "assistant":
        print(f"최종 반환 정보:\n{message.content}\n")