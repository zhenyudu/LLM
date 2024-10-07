
class ModelGenerator:

    def __init__(self, model):
        self.model = model

    def generate(self, query, **params):
        return self.model.invoke(query, **params)

    def rag_generate(self, retriever, question, **params):
        retrieval = retriever.similarity_search_with_relevance_scores(question, k=5)
        context = "\n\n".join( [doc[0].page_content for doc in retrieval] )
        prompt = f"""
        只能使用繁體中文回答問題。
        請根據參考文件回答使用者問題。
        參考文件：\n{context}\n
        使用者問題：{question}
        你的回答：
        """
        return self.model.invoke(prompt, **params)