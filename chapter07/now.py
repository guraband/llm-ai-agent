from gpt_function import get_current_time, tools
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("STUDY_OPENAI_API_KEY"))


def get_ai_response(messages, tools=None):

    print("\n# messages : ", messages)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        # model="gpt-4o",
        messages=messages,
        tools=tools,
    )
    return response


messages = [
    {"role": "system", "content": "당신은 유능한 인공지능 에이전트입니다."}
]

while True:
    user_input = input("사용자 : ")
    if user_input == "q" or user_input == "Q" or user_input == "bye" or user_input == "exit":
        break

    messages.append({"role": "user", "content": user_input})

    ai_response = get_ai_response(messages, tools=tools)
    ai_message = ai_response.choices[0].message
    print(f"AI : {ai_message}")

    tool_calls = ai_message.tool_calls
    if tool_calls:
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            tool_call_id = tool_call.id
            args = json.loads(tool_call.function.arguments)

            if tool_name == "get_current_time":
                messages.append({
                    "role": "function",
                    "tool_call_id": tool_call_id,
                    "name": tool_name,
                    "content": get_current_time(timezone=args["timezone"]),
                })

        messages.append({"role": "system", "content": "주어진 결과를 바탕으로 답변해주세요."})

        ai_response = get_ai_response(messages, tools=tools)
        ai_message = ai_response.choices[0].message

    print(f"\nAI : {ai_message.content}")
    if ai_message.content:
        messages.append({"role": "assistant", "content": ai_message.content})
