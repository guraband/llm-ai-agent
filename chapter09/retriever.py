from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv
import os


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
embedding = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key=OPENAI_API_KEY,
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
persist_directory = "/Users/ng/Documents/workspace/ai/llm-ai-agent/chapter09/chroma_store"

vectorstore = Chroma(
    persist_directory=persist_directory,
    embedding_function=embedding,
)

retriever = vectorstore.as_retriever(k=3)

question_answering_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "사용자의 질문에 대해 아래 context에 기반하여 답변해주세요.\n\n{context}"),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

document_chain = create_stuff_documents_chain(
    llm, question_answering_prompt) | StrOutputParser()

query_augmentation_prompt = ChatPromptTemplate.from_messages(
    [
        MessagesPlaceholder(variable_name="messages"),
        (
            "system",
            """기존 대화 내용을 활용하여 사용자가 질문한 의도를 파악해서 한 문장의 명료한 질문으로 변환하라.
            대명사나 이, 저, 그와 같은 표현을 명확한 명사로 표현하라.\n\n{query}
            """
        )
    ]
)

query_augmentation_chain = query_augmentation_prompt | llm | StrOutputParser()
