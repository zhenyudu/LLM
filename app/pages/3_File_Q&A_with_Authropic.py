# import streamlit as st
# import anthropic
# from model.ModelLoader import ModelLoader
# from model.ModelGenerator import ModelGenerator

# ##  Sidebar  ##
# with st.sidebar:
#     st.subheader('⚙︎ Models and parameters')
#     selected_model = st.sidebar.selectbox('Choose a Model with Ollama', ['Llama3.2:latest', 'Llama3.1:latest', 'Llama2:7b-chat'], key='selected_model')

#     ## Load Model & Retriever
#     model = ModelLoader.ollama_loader(model_name = selected_model)
#     llm = ModelGenerator(model=model)

#     temperature     = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.75, step=0.01)
#     top_p           = st.sidebar.slider("Top_P", min_value=0.0, max_value=1.0, value=0.95, step=0.01)
#     top_k           = st.sidebar.slider("Top_K", min_value=0, max_value=100, value=50, step=1)
#     max_tokens      = st.sidebar.slider("Max_Tokens", min_value=0, max_value=4096, value=256, step=1, disabled=True)
#     repeat_penalty  = st.sidebar.slider("Repeat_Penalty", min_value=0.0, max_value=2.0, value=1.1, step=0.1)


# ##  Main Page  ##
# st.title("📝 File Q&A with Authropic")
# uploaded_file = st.file_uploader("Upload an article", type=("txt", "md"))
# question = st.text_input(
#     "Ask something about the article",
#     placeholder="Can you give me a short summary?",
#     disabled=not uploaded_file,
# )


# if uploaded_file and question:
#     article = uploaded_file.read().decode()
#     prompt = f"""{anthropic.HUMAN_PROMPT} Here's an article:\n\n<article>
#     {article}\n\n</article>\n\n{question}{anthropic.AI_PROMPT}"""

#     response = response = llm.generate(query=prompt, **{
#         "temperature":temperature, "top_p":top_p, "top_k":top_k, "max_length":max_tokens, "repetition_penalty":repeat_penalty
#     })
#     st.write("### Answer")
#     st.write(response.completion)