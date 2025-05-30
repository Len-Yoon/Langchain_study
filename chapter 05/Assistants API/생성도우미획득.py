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

# 도우미 출력
# print(assistant)
