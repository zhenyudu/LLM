from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from .embedding import embedding_loader

def get_retriever():

    file_path = (
        "/Users/duzhenyu/Desktop/Projects/LLM/app/data/pdf/勞動基準法.pdf"
    )
    loader = PyPDFLoader(file_path)
    splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
    docs = loader.load_and_split(splitter)

    embedding = embedding_loader(model_name="BAAI/bge-large-zh-v1.5")
    vector_store = FAISS.from_documents(docs, embedding)

    return vector_store

if __name__ == "__main__":
    vector_store = get_retriever()
    retrievals = vector_store.similarity_search_with_relevance_scores("離職天數規定", k=5)
    print(retrievals)