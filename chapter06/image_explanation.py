from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("STUDY_OPENAI_API_KEY"))

messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "다음 이미지를 설명해줘"},
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://images.unsplash.com/photo-1736264335247-8ec5664c8328?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                }
            }
        ]
    }
]

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
)

print(response.choices[0].message.content)
