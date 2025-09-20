from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# 대화 히스토리를 저장할 리스트
messages = [SystemMessage(content="You are a helpful assistant.")]
MAX_MESSAGES = 20  # 최대 메시지 수 (시스템 메시지 제외)


def manage_message_history():
    """메시지 히스토리를 관리하여 토큰 제한을 방지"""
    # 시스템 메시지 + 최근 대화만 유지
    if len(messages) > MAX_MESSAGES + 1:  # +1은 시스템 메시지
        # 시스템 메시지와 최근 대화만 유지
        messages[:] = [messages[0]] + messages[-(MAX_MESSAGES):]


def clear_history():
    """대화 히스토리 초기화"""
    global messages
    messages = [SystemMessage(content="You are a helpful assistant.")]
    print("대화 히스토리가 초기화되었습니다.")


def show_history():
    """현재 대화 히스토리 보기"""
    print(f"\n현재 대화 수: {len(messages) - 1}개")
    for i, msg in enumerate(messages[1:], 1):  # 시스템 메시지 제외
        role = "사용자" if isinstance(msg, HumanMessage) else "AI"
        content = msg.content[:50] + \
            "..." if len(msg.content) > 50 else msg.content
        print(f"{i}. {role}: {content}")
    print()


model = ChatOllama(model="gemma3:4b")

while True:
    user_input = input("- 사용자 : ")
    if user_input.lower() in ["exit", "q", "quit", "bye", "ㅂ"]:
        break

    # 특별 명령어 처리
    if user_input.lower() in ["/clear", "/초기화"]:
        clear_history()
        continue
    elif user_input.lower() in ["/history", "/히스토리"]:
        show_history()
        continue
    elif user_input.lower() in ["/help", "/도움말"]:
        print("\n사용 가능한 명령어:")
        print("- /clear 또는 /초기화: 대화 히스토리 초기화")
        print("- /history 또는 /히스토리: 현재 대화 히스토리 보기")
        print("- /help 또는 /도움말: 이 도움말 보기")
        print("- exit, q, quit, bye, ㅂ: 프로그램 종료")
        print()
        continue

    # 사용자 메시지를 히스토리에 추가
    messages.append(HumanMessage(content=user_input))

    print("- AI : ", end="", flush=True)

    # AI 응답을 스트리밍으로 받기
    ai_response = ""
    try:
        for chunk in model.stream(messages):
            if hasattr(chunk, 'content') and chunk.content:
                print(chunk.content, end="", flush=True)
                ai_response += chunk.content
    except Exception as e:
        # stream이 실패하면 invoke로 대체
        print(f"Stream error: {e}")
        response = model.invoke(messages)
        ai_response = response.content if hasattr(
            response, 'content') else str(response)
        print(ai_response, end="", flush=True)

    # AI 응답을 히스토리에 추가
    if ai_response:
        messages.append(AIMessage(content=ai_response))

    # 메시지 히스토리 관리
    manage_message_history()

    print("\n")
