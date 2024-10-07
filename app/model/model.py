from langchain_community.chat_models import ChatOllama

def model_loader(model_name: str = "llama3.2", **params):
    model = ChatOllama(model=model_name, **params)
    return model

if __name__ == "__main__":
    model = model_loader()
    response = model.invoke("hello")
    print(response)