import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage

import retriever

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)


def get_ai_response(messages):
    response = llm.stream(messages)

    for chunk in response:
        yield chunk


st.title("Langchain RAG Practice")
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        SystemMessage("너는 문서에 기반해 답변하는 도시 정책 전문가야."),
    ]

for msg in st.session_state["messages"]:
    if msg.content:
        if isinstance(msg, SystemMessage):
            st.chat_message("system").write(msg.content)
        elif isinstance(msg, HumanMessage):
            st.chat_message("user").write(msg.content)
        elif isinstance(msg, AIMessage):
            st.chat_message("assistant").write(msg.content)

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    st.session_state.messages.append(HumanMessage(prompt))

    print("user\t:", prompt)

    augmented_query = retriever.query_augmentation_chain.invoke(
        {"messages": st.session_state["messages"],
         "query": prompt}
    )

    print("augmented_query\t:", augmented_query)

    with st.spinner(f"AI가 답변을 준비 중입니다... '{augmented_query}'"):
        response = get_ai_response(st.session_state["messages"])
        result = st.chat_message("assistant").write_stream(response)
    st.session_state["messages"].append(AIMessage(result))
