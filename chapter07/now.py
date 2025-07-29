from gpt_function import get_current_time, tools, get_yf_stock_info
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import streamlit as st

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


st.title("💬 Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "당신은 유능한 인공지능 에이전트입니다."}
    ]

for msg in st.session_state.messages:
    if msg["role"] == "assistant" or msg["role"] == "user":
        st.chat_message(msg["role"]).write(msg["content"])

if user_input := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    ai_response = get_ai_response(st.session_state.messages, tools=tools)
    print(ai_response)
    ai_message = ai_response.choices[0].message

    tool_calls = ai_message.tool_calls
    if tool_calls:
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            tool_call_id = tool_call.id
            args = json.loads(tool_call.function.arguments)

            if tool_name == "get_current_time":
                function_response = get_current_time(timezone=args["timezone"])
            elif tool_name == "get_yf_stock_info":
                function_response = get_yf_stock_info(args["ticker"])

            st.session_state.messages.append({
                "role": "function",
                "tool_call_id": tool_call_id,
                "name": tool_name,
                "content": function_response,
            })

        st.session_state.messages.append(
            {"role": "system", "content": "주어진 결과를 바탕으로 답변해주세요."})

        ai_response = get_ai_response(st.session_state.messages, tools=tools)
        ai_message = ai_response.choices[0].message

    if ai_message.content:
        st.session_state.messages.append(
            {"role": "assistant", "content": ai_message.content})
        st.chat_message("assistant").write(ai_message.content)
    else:
        # content가 None인 경우 기본 메시지 표시
        error_message = "죄송합니다. 응답을 생성하는 중 문제가 발생했습니다. 다시 시도해 주세요."
        st.session_state.messages.append(
            {"role": "assistant", "content": error_message})
        st.chat_message("assistant").write(error_message)
