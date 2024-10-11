import streamlit as st
from model.ModelLoader import ModelLoader
from model.ModelGenerator import ModelGenerator



##  Sidebar  ##
with st.sidebar:

    st.subheader('⚙︎ Models and parameters')
    selected_model = st.sidebar.selectbox('Choose a Model with Ollama', ['Llama3.2:latest', 'Llama3.1:latest', 'Llama2:7b-chat'], key='selected_model')

    ## Load Model & Retriever
    model = ModelLoader.ollama_loader(model_name = selected_model)
    llm = ModelGenerator(model=model)

    temperature     = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.75, step=0.01)
    top_p           = st.sidebar.slider("Top_P", min_value=0.0, max_value=1.0, value=0.95, step=0.01)
    top_k           = st.sidebar.slider("Top_K", min_value=0, max_value=100, value=50, step=1, disabled=True)
    max_tokens      = st.sidebar.slider("Max_Tokens", min_value=0, max_value=4096, value=512, step=1)
    repeat_penalty  = st.sidebar.slider("Repeat_Penalty", min_value=0.0, max_value=2.0, value=1.1, step=0.1, disabled=True)


##  Main Content  ##
st.title("⛅️ QA Chatbot")
st.markdown("""
<style>
    .st-emotion-cache-janbn0 {
        flex-direction: row-reverse;
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)

# Store LLM generated responses
initialize_messages = [{"role": "assistant", "content": "How may I assist you today?"}]
if "messages" not in st.session_state.keys():
    st.session_state.messages = initialize_messages

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# clear chat history
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)


# User input and add to chat messages
if prompt := st.chat_input(placeholder="say something ..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)



def generate_response(prompt_input):
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    
    string_dialogue += "User:  {}\n\nAssistant: ".format(prompt_input)

    response = llm.generate(query=string_dialogue, **{
        "temperature":temperature, "top_p":top_p, "top_k":top_k, "max_length":max_tokens, "repetition_penalty":repeat_penalty
    })

    return response.content


# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)