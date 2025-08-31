from langgraph.checkpoint.memory import MemorySaver
from langchain.schema import HumanMessage
from langchain_openai import ChatOpenAI
from typing import Annotated  # 타입 힌트 사용을 위한 모듈
from typing_extensions import TypedDict  # 딕셔너리 타입 정의를 위한 모듈

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


model = ChatOpenAI(model="gpt-4o-mini")


class State(TypedDict):
    messages: Annotated[list[str], add_messages]


graph_builder = StateGraph(State)


def generate(state: State):
    """
    주어진 상태를 기반으로 챗봇의 응답 메시지를 생성합니다.
    """
    return {"messages": [model.invoke(state["messages"])]}


graph_builder.add_node("generate", generate)

graph_builder.add_edge(START, "generate")
graph_builder.add_edge("generate", END)

memory = MemorySaver()
config = {"configurable": {"thread_id": "temp"}}

graph = graph_builder.compile(checkpointer=memory)


while True:
    user_input = input("You\t: ")
    if user_input.lower() in ["exit", "quit", "q"]:
        break

    for event in graph.stream({"messages": [HumanMessage(content=user_input)]}, config, stream_mode="values"):
        event["messages"][-1].pretty_print()

    print(f"\n현재 메시지 개수 : {len(event['messages'])}\n----------------\n")
