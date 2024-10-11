import streamlit as st
from langchain_community.chat_models import ChatOllama
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import HumanMessage
import asyncio

class StreamHandler(StreamingStdOutCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        print(token, end="", flush=True)
        self.text += token
        self.container.markdown(self.text + "▌")

async def stream_response(prompt, chat_history):
    llm = ChatOllama(
        model="llama3.2",
        streaming=True,
        callbacks=[StreamHandler(st.empty())],
    )
    messages = chat_history + [HumanMessage(content=prompt)]
    await llm.agenerate([messages])
    return llm

st.title("ChatOllama Streaming Demo")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Enter your message:")

if st.button("Send"):
    if user_input:
        st.session_state.chat_history.append(HumanMessage(content=user_input))
        asyncio.run(stream_response(user_input, st.session_state.chat_history))
        st.session_state.chat_history.append(HumanMessage(content=user_input))
    else:
        st.warning("Please enter a message.")

if st.button("Clear Chat History"):
    st.session_state.chat_history = []
    st.success("Chat history cleared.")

st.subheader("Chat History:")
for message in st.session_state.chat_history:
    st.write(f"Human: {message.content}")