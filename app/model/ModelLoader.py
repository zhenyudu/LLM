from langchain_community.chat_models import ChatOllama

class ModelLoader:

    @classmethod
    def ollama_loader(cls, model_name: str = "llama3.2", **params):
        model = ChatOllama(model=model_name, **params)
        return model
    
    classmethod
    def llamacpp_loader(cls, model_name: str, **params):
        pass

    @classmethod
    def transformer_loader(cls, model_name: str, **params):
        pass
