# 환경 변수 설정
import os
from dotenv import load_dotenv
from openai.resources.beta import assistants

load_dotenv("../key.env")

# LLM 설정
from openai import OpenAI
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# 데이터 파일 적재 및 내용 표시
import pandas as pd

file_path='data/sales_data.csv'
sales_data=pd.read_csv(file_path)

sales_data

# 파일 생성
file = client.files.create(
    file=open(file_path, 'rb'),
    purpose='assistants'
)

# 파일을 포함한 도우미 생성
assistant = client.beta.assistants.create(
    instructions='데이터 과학 도우미로서, 주어진 데이터와 요청에 따라 '
                 +'적절한 코드를 작성하고 적절한 시각화를 생성할 수 있습니다.',
    model='gpt-4o-mini',
    tools=[
        {'type':'code_interpreter'}
    ],
    tool_resources={
        'code_interpreter' : {'file_ids':[file.id]} # 여기에 파일의 ID 추가
    }
)

print(assistant)

# 대화 흐름 생성
thread = client.beta.threads.create(
    messages=[
        {
            'role': 'user',
            'content': '2022년부터 2025년까지 각 분기의 총 판매액을 계산하고, 이를 다른 제품으로 시각화하여 선 그래프로 표시하세요. 제품의 선 색상은 각각 빨강, 파랑, 녹색으로 설정하세요.',
            'attachments': [
                {
                    'file_id': file.id,
                    'tools': [
                        {'type': 'code_interpreter'}
                    ]
                }
            ]
        }
    ]
)

print(thread)

# 실행 세션 생성
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
)

# 실행 세션 출력
print(run)

import time

while True:
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )

    try:
        # 이미지 파일 생성 확인
        if messages.data[0].content[0].image_file:
            print('차트가 생성되었습니다!')

            if messages.data and messages.data[0].content:
                print("현재 메세지", messages.data[0].content[0])
            break
    except:
        time.sleep(10)
        print('도우미가 차트를 열심히 작성하고 있어요!')
        if messages.data and messages.data[0].content:
            print("현재 메세지:", messages.data[0].content[0])

    # 순환 전 잠시 대기
    time.sleep(5)

# 파일을 PNG 형식으로 변환하는 함수
def convert_file_to_png(file_id, write_path):
    data = client.files.content(file_id)
    data_bytes = data.read()

    with open(write_path, 'wb') as file:
        file.write(data_bytes)

# 첫 번째 메시지에서 이미지 파일 ID 가져오기
plot_file_id = messages.data[0].content[0].image_file.file_id
image_path = '태진_도서_판매2.png'

# 파일을 PNG로 변환
convert_file_to_png(plot_file_id, image_path)

# 차트 업로드
plot_file = client.files.create(
    file=open(image_path, 'rb'),
    purpose='assistants'
)

# 도우미의 생각과 행동 과정 표시
messages = client.beta.threads.messages.list(thread_id=thread.id)
assistant_thoughts_and_actions = [message.content[0] for message in messages.data]

# 결과 출력
for content in assistant_thoughts_and_actions:
    print("content",content)

## 자동으로 데이터 통찰 생성하기
import time

def sumbit_message_wait_completion(assistant_id, thread, user_message, file_ids=None):
    # 활성화된 실행 세션이 완료될 때까지 대기
    for run in client.beta.threads.runs.list(thread_id=thread.id).data:
        if run.status == 'in_progress':
            print(f"실행 세션 {run.id} 완료 대기 중...")

        while True:
            run_status = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id).status

            if run_status in ['succeeded','failed']:
                break

            time.sleep(5) # 5초간 대기

    #메세지 제출
    params = {
        'thread_id': thread.id,
        'role': 'user',
        'content': user_message
    }

    # 첨부 파일 설정
    if file_ids:
        attachments = [{"file_id": file_id, 'tools':[{"type":"code_interpreter"}]} for file_id in file_ids]
        params['attachments'] = attachments

    client.beta.threads.messages.create(**params)

    # 실행 세션 생성
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant_id)
    return run

# 요청을 보내 도우미에게 통찰 생성을 요청
sumbit_message_wait_completion(
    assistant.id,
    thread,
    '앞에서 생성한 차트를 기반으로 약 20자 내외의 문장 두 개로 가장 중요한 통찰을 설명해 주세요. 이 내용은 프레젠테이션 발표에서 데이터의 비밀을 드러내기 위해 사용될 것입니다.'
)

# 대화 흐름의 응답을 가져오는 함수
def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id)

# 응답 대기 후 생성된 통찰 출력
time.sleep(10) # 데이터 과학 도우미가 통찰을 생성하는 데 시간이 필요하다고 가정

response = get_response(thread)
bullet_points = response.data[0].content[0].text.value

print(bullet_points)

# 통찰에 기반한 제목 생성
submit_message_wait_completion(
    assistant_id=assistant.id,
    thread=thread,
    user_message='당신이 만든 차트와 통찰을 바탕으로, 주요 통찰을 반영하는 아주 짧은 프레젠테이션 제목을 만들어 주세요.'
)

# 응답 대기 후 생성된 제목 출력
time.sleep(10)  # 도우미가 제목을 생성하는 데 시긴이 필요하다고 가정

response = get_response(thread)
title = response.data[0].content[0].text.value

print(title)