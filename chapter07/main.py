from gpt_function import get_current_time, tools, get_yf_stock_info, get_yf_stock_history, get_yf_stock_recommendations
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import streamlit as st
from typing import List, Dict, Any, Optional
from collections import defaultdict

# 상수 정의
DEFAULT_MODEL = "gpt-4o-mini"
SYSTEM_MESSAGE = "당신은 유능한 인공지능 에이전트입니다."
FUNCTION_RESULT_PROMPT = "주어진 결과를 바탕으로 답변해주세요."
ERROR_MESSAGE = "죄송합니다. 응답을 생성하는 중 문제가 발생했습니다. 다시 시도해 주세요."

load_dotenv()
client = OpenAI(api_key=os.getenv("STUDY_OPENAI_API_KEY"))


def tool_list_to_tool_obj(tools):
    tool_calls_dict = defaultdict(lambda: {"id": None, "function": {
                                  "arguments": "", "name": None}, "type": None})

    for tool_call in tools:
        if tool_call.id is not None:
            tool_calls_dict[tool_call.index]["id"] = tool_call.id

        if tool_call.function.name is not None:
            tool_calls_dict[tool_call.index]["function"]["name"] = tool_call.function.name

        tool_calls_dict[tool_call.index]["function"]["arguments"] += tool_call.function.arguments

        if tool_call.type is not None:
            tool_calls_dict[tool_call.index]["type"] = tool_call.type

    tool_calls_list = list(tool_calls_dict.values())
    return {"tool_calls": tool_calls_list}


def get_ai_response(messages: List[Dict[str, str]],
                    tools: Optional[List] = None,
                    stream: bool = True) -> Any:
    """AI 응답을 가져오는 함수"""
    try:
        print("\n# messages : ", messages)
        response = client.chat.completions.create(
            model=DEFAULT_MODEL,
            stream=stream,
            messages=messages,
            tools=tools,
        )

        if stream:
            for chunk in response:
                yield chunk
        else:
            return response
    except Exception as e:
        print(f"AI 응답 생성 중 오류: {e}")
        return None


def execute_function_call(tool_name: str, args: Dict[str, Any]) -> str:
    """Function call 실행 함수"""
    try:
        if tool_name == "get_current_time":
            return get_current_time(timezone=args["timezone"])
        elif tool_name == "get_yf_stock_info":
            return get_yf_stock_info(args["ticker"])
        elif tool_name == "get_yf_stock_history":
            return get_yf_stock_history(args["ticker"], args["period"])
        elif tool_name == "get_yf_stock_recommendations":
            return get_yf_stock_recommendations(args["ticker"])
        else:
            return f"알 수 없는 함수: {tool_name}"
    except Exception as e:
        print(f"함수 실행 중 오류 ({tool_name}): {e}")
        return f"함수 실행 중 오류가 발생했습니다: {str(e)}"


def process_tool_calls(tool_calls: Any, messages: List[Dict[str, str]]) -> None:
    """Tool calls 처리 함수"""
    if not tool_calls:
        return

    for tool_call in tool_calls:
        tool_name = tool_call["function"]["name"]
        tool_call_id = tool_call["id"]

        try:
            arguments = json.loads(tool_call["function"]["arguments"])
            function_response = execute_function_call(tool_name, arguments)

            messages.append({
                "role": "function",
                "tool_call_id": tool_call_id,
                "name": tool_name,
                "content": function_response,
            })
        except json.JSONDecodeError as e:
            print(f"JSON 파싱 오류: {e}")
            messages.append({
                "role": "function",
                "tool_call_id": tool_call_id,
                "name": tool_name,
                "content": "함수 인수 파싱 중 오류가 발생했습니다.",
            })


def handle_ai_response(messages: List[Dict[str, str]]) -> None:
    """AI 응답 처리 함수"""
    ai_response = get_ai_response(messages, tools=tools)

    content = ""
    tool_calls = None
    tool_calls_chunk = []

    with st.chat_message("assistant").empty():
        for chunk in ai_response:
            content_chunk = chunk.choices[0].delta.content
            if content_chunk:
                print(content_chunk, end="")
                content += content_chunk
                st.markdown(content)

            if chunk.choices[0].delta.tool_calls:
                tool_calls_chunk += chunk.choices[0].delta.tool_calls

        tool_obj = tool_list_to_tool_obj(tool_calls_chunk)
        tool_calls = tool_obj["tool_calls"]

        if len(tool_calls) > 0:
            tool_call_msg = [tool_call["function"] for tool_call in tool_calls]
            st.write(tool_call_msg)

    if not ai_response:
        display_error_message(messages)
        return

    print(ai_response)
    # ai_message = ai_response.choices[0].message

    print(tool_calls)

    # Tool calls 처리
    if tool_calls:
        process_tool_calls(tool_calls, messages)

        # Function 결과를 바탕으로 다시 응답 생성
        messages.append({"role": "system", "content": FUNCTION_RESULT_PROMPT})

        final_response = get_ai_response(messages, tools=tools)
        if final_response:
            # ai_message = final_response.choices[0].message
            content = ""
            with st.chat_message("assistant").empty():
                for chunk in final_response:
                    content_chunk = chunk.choices[0].delta.content
                    if content_chunk:
                        print(content_chunk, end="")
                        content += content_chunk
                        st.markdown(content)
        else:
            display_error_message(messages)
            return

    # 최종 응답 처리
    if content:
        messages.append({"role": "assistant", "content": content})
        # st.chat_message("assistant").write(content)
    else:
        display_error_message(messages)


def display_error_message(messages: List[Dict[str, str]]) -> None:
    """오류 메시지 표시 함수"""
    messages.append({"role": "assistant", "content": ERROR_MESSAGE})
    st.chat_message("assistant").write(ERROR_MESSAGE)


def initialize_session_state() -> None:
    """세션 상태 초기화 함수"""
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": SYSTEM_MESSAGE}
        ]


def display_chat_history() -> None:
    """채팅 기록 표시 함수"""
    for msg in st.session_state.messages:
        if msg["role"] in ["assistant", "user"]:
            st.chat_message(msg["role"]).write(msg["content"])


def main() -> None:
    """메인 함수"""
    st.title("💬 Chatbot")

    # 세션 상태 초기화
    initialize_session_state()

    # 채팅 기록 표시
    display_chat_history()

    # 사용자 입력 처리
    if user_input := st.chat_input():
        st.session_state.messages.append(
            {"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)

        # AI 응답 처리
        handle_ai_response(st.session_state.messages)


if __name__ == "__main__":
    main()
