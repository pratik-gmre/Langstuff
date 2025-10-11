import streamlit as st
from server import chatbot
from langchain_core.messages import HumanMessage
import uuid

# ---------- Helper Functions ----------

def create_thread_id():
    return str(uuid.uuid4())

def add_thread(thread_id):
    if "chat_threads" not in st.session_state:
        st.session_state["chat_threads"] = []
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)

def reset_chat():
    thread_id = create_thread_id()
    st.session_state["thread_id"] = thread_id
    add_thread(thread_id)
    st.session_state["message_history"] = []

def load_conversation(thread_id):
    CONFIG = {"configurable": {"thread_id": thread_id}}
    state = chatbot.get_state(config=CONFIG)
    if "messages" in state.values:
        messages = state.values["messages"]
        formatted = []
        for m in messages:
            role = "user" if isinstance(m, HumanMessage) else "assistant"
            formatted.append({"role": role, "content": m.content})
        return formatted
    return []

# ---------- Session Initialization ----------

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = create_thread_id()

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = []

add_thread(st.session_state["thread_id"])

# ---------- Sidebar ----------

st.sidebar.title("🤖 ChatBot")

if st.sidebar.button("➕ New Chat"):
    reset_chat()

st.sidebar.header("💬  Chats")

for thread_id in st.session_state["chat_threads"]:
    if st.sidebar.button(thread_id):
        st.session_state["thread_id"] = thread_id
        st.session_state["message_history"] = load_conversation(thread_id)

# ---------- Main Chat Area ----------

st.title("AI Chatbot")

# Display messages
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message
    st.session_state["message_history"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate assistant response
    CONFIG = {"configurable": {"thread_id": st.session_state["thread_id"]}}
    with st.chat_message("assistant"):
        ai_message = st.write_stream(
            chunk.content
            for chunk, _ in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages",
            )
        )

    # Save assistant message
    st.session_state["message_history"].append(
        {"role": "assistant", "content": ai_message}
    )
