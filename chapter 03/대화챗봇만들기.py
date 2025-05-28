# OpenAI 키 설치
import os
from dotenv import load_dotenv
load_dotenv("../key.env")

openai_api_key = os.getenv("OPENAI_API_KEY")

# OpenAI 가져오기
from openai import OpenAI

# Client 인스턴스 생성하기
client = OpenAI(api_key=openai_api_key)

# chat.completions.create 메서드를 호출하여 응답을 받음
response = client.chat.completions.create(
    model="gpt-4o-mini",
    response_format={"type":"json_object"},
    messages=[
        {"role":"system", "content":"당신은 사용자가 꽃에 대한 정보를 이해하도록 돕는 지능형 비서이며, JSON 형식의 내용을 출력 할 수 있습니다."},
        {"role":"user","content":"생일 선물로 어떤 꽃이 가장 좋나요?"},
        {"role":"assistant", "content":"장미꽃은 생일 선물로 인기 있는 선택입니다."}
    ]
)

print(response.choices[0].message.content)