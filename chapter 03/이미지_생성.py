# OpenAI 키 설치
import os
from dotenv import load_dotenv
import requests

load_dotenv("../key.env")

openai_api_key = os.getenv("OPENAI_API_KEY")

# OpenAI 가져오기
from openai import OpenAI

# Client 인스턴스 생성하기
client = OpenAI(api_key=openai_api_key)

response = client.images.generate(
    model="dall-e-3",
    prompt="기타치는 곰인형",
    size="1024x1024",
    quality="standard",
    n=1
)

# 응답 구조 확인
print(response)

# 이미지 URL 가져오기 (응답 구조에 따라 다를 수 있음)
image_url = response.data[0].url

# 이미지 다운로드 및 저장
image_response = requests.get(image_url)
if image_response.status_code == 200:
    with open("../guitar_bear.png", "wb") as f:
        f.write(image_response.content)
    print("이미지 저장 완료: guitar_bear.png")
else:
    print("이미지 다운로드 실패")