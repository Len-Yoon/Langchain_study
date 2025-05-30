# 환경 변수 설정
import os
from dotenv import load_dotenv
from openai.resources.beta import assistants

load_dotenv("../key.env")

# LLM 설정
from openai import OpenAI
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# 회사 설명 제공
company_summary = '곰돌이 인형같은 우리 귀여훈 회장님은 기타를 잘치지만, IT에도 관심이 많습니다.'

# DALL.E 3 모델을 호출하여 이미지 생성
response = client.images.generate(
    model='dall-e-3',
    prompt=f'이 회사의 설명인 {company_summary}을 바탕으로, 회사가 직원들과'
           f'함께 성장하고 전진하고 있다는 영감을 주는 이미지를 만들어주세요.',
    size='1024x1024',
    quality='hd',
    n=1
)

# DALL.E 3 모델이 생성한 이미지 url 가져오기
image_url = response.data[0].url

# DALL.E 3 모델이 생성한 이미지 가져오기
import requests

dall_img_path = '기타치는곰탱이.png'
img = requests.get(image_url)

# 이미지 저장
with open(dall_img_path, 'wb') as file:
    file.write(img.content)

# 업로드한 이미지를 프레젠테이션 자료로 활용
dalle_file = client.files.create(
    file=open(dall_img_path, 'rb'),
    purpose='assistants'
)