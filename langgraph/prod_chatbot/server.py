from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from dotenv import load_dotenv


load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage
from langgraph.checkpoint.memory import InMemorySaver


from langgraph.graph.message import add_messages


class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


llm = ChatOpenAI(model="gpt-4")


def chat_node(state: ChatState):
    messages = state["messages"]
    response = llm.invoke(messages)

    return {"messages": [response]}


# checkpointer
checkpointer = InMemorySaver()

graph = StateGraph(ChatState)
# add nodes
graph.add_node("chat_node", chat_node)

# add edges
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)


