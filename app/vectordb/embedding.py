from langchain_huggingface import HuggingFaceEmbeddings

def embedding_loader(
        model_name      = "BAAI/bge-large-zh-v1.5",
        model_kwargs    = {'device': 'cpu'},
        encode_kwargs   = {'normalize_embeddings': False} ):
    
    embedding = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    return embedding